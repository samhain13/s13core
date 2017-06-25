from django.core.management import call_command
from django.core.management.base import BaseCommand
from s13core.settings.models import Setting, ContactInfo, CopyrightInfo
from s13core.content_management.models import User


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
        call_command('createsuperuser')

    def create_initial_settings(self):
        self.stdout.write('** Collecting initial settings values.')
        site_title = self._prompt_info('Website Title')
        site_description = self._prompt_info('Description', False)
        site_keywords = self._prompt_info('Keywords', False)
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
        statement = self._prompt_info('Copyright Statement')
        if self._prompt_info('Use Creative Commons? [yes/no]')\
                .lower().startswith('y'):
            cl = 'Creative Commons Attribution Share-Alike License'
            lc = 'https://creativecommons.org/licenses/by-sa/4.0/legalcode'
        else:
            cl = ''
            lc = ''
        co = CopyrightInfo(statement=statement, license=cl, link=lc)
        co.save()
        return co

    def _prompt_info(self, question, is_required=True):
        p = '{}{}: '.format(question, ' (required)' if is_required else '')
        s = input(p)
        if is_required:
            while not s:
                s = input(p)
        return s
