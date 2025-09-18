from getpass import getpass

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand

from s13core.settings.models import ContactInfo
from s13core.settings.models import CopyrightInfo
from s13core.settings.models import Setting


class Command(BaseCommand):
    help = 'Sets up a new S13Core website; applies migrations, creates ' + \
        'a superuser, and creates the initial website settings.'

    def handle(self, *args, **options):
        self.create_database()
        self.create_initial_settings()

    def create_database(self):
        self.stdout.write('** Applying migrations, if any.')
        call_command('makemigrations')
        call_command('migrate')
        self.stdout.write('** Creating the main superuser account.')
        self._create_superuser()

    def create_initial_settings(self):
        self.stdout.write('** Collecting initial settings values.')
        site_title = self._prompt_info('Website Title')
        site_description = self._prompt_info('Description', False)
        site_keywords = self._prompt_info('Keywords', False)
        # Make sure we have no Initial Settings.
        old_inits = Setting.objects.filter(name='Initial Settings')
        if old_inits:
            self.stdout.write('** Old Initial Settings found, moving...')
            for o in old_inits:
                old_name = o.name
                o.name = '{} - {}'.format(old_name, o.pk)
                o.save()
                self.stdout.write(
                    '   - Moved "{}" to "{}"'.format(old_name, o.name)
                )
        s = Setting(
            name='Initial Settings', is_active=True, title=site_title,
            description=site_description, keywords=site_keywords,
            copyright=self._create_copyright_statement(),
            css='<link rel="stylesheet" href="/static/css/default.css" />'
        )
        s.save()
        s.contact.add(self._create_admin_contact())

    def _create_admin_contact(self):
        admin = User.objects.all()[0]
        contact = ContactInfo(
            contact_name='Website Administrator',
            email=admin.email
        )
        contact.save()
        return contact

    def _create_copyright_statement(self):
        statement = self._prompt_info('Copyright Statement', False)
        if self._prompt_yesno('Use Creative Commons?'):
            cl = 'Creative Commons Attribution Share-Alike License'
            lc = 'https://creativecommons.org/licenses/by-sa/4.0/legalcode'
        else:
            cl = ''
            lc = ''
        # Try to use an existing copyright statement, if possible.
        old_statement = CopyrightInfo.objects.filter(
            statement=statement, license=cl).last()
        if old_statement:
            return old_statement
        else:
            co = CopyrightInfo(statement=statement, license=cl, link=lc)
            co.save()
            return co

    def _create_superuser(self):
        username = self._prompt_info('Username')
        email = self._prompt_info('Email')
        password = self._prompt_info('Password')
        user = User.objects.filter(username=username).first()
        if user:
            self.stdout.write(
                '** Username "{}" already exists.'.format(username))
            if self._prompt_yesno('Would you like to save your new info?'):
                user.email = email
                user.set_password(password)
                user.save()
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            user.is_superuser = True
            user.is_staff = True
            user.save()

    def _prompt_info(self, question, is_required=True):
        use_input = input if 'password' not in question.lower() else getpass
        p = '{}{}: '.format(question, ' (required)' if is_required else '')
        s = use_input(p)
        if is_required:
            while not s:
                s = use_input(p)
        return s

    def _prompt_yesno(self, question):
        return self._prompt_info(
            '{} [yes/no]'.format(question)
        ).lower().startswith('y')
