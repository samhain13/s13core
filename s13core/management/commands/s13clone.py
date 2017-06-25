import os
import shutil
from random import choice
from django.core.management.base import BaseCommand
from django.conf import settings as s


class Command(BaseCommand):
    help = 'Creates a new S13Core project by cloning this package into ' + \
        'a new location.'

    def add_arguments(self, parser):
        parser.add_argument(
            'project', help='project name, like: ' +
            'www.example.com; non-alphanumeric characters will be stripped ' +
            'when making the module name'
        )
        parser.add_argument(
            '-w', '--overwrite', action='store_true',
            help='overwrite project if it exists'
        )

    def handle(self, *args, **options):
        self.project = os.path.realpath(options['project'])
        self.is_overwrite = options['overwrite']
        self.source = os.getcwd()
        # Validate the source paths.
        self.get_source_paths()
        # Generate a valid module name.
        self.generate_module_name()
        # Create the project directory.
        self.make_project_dir()
        # Replace source website references with the project name.
        self.replace_values()
        self.stdout.write(
            '** Cloning complete.\n\nYou may now run ' +
            './manage.py s13setup in\n{}\nGoodbye.\n'.format(self.project)
        )

    def generate_module_name(self):
        self.stdout.write('** Generating the module name from project name.')
        n = ''
        if self.source == self.project:
            raise ValueError('Cannot create project in source directory.')
        for l in os.path.basename(self.project):
            if l.isalnum() or l == '_':
                n += l
        if not n:
            raise ValueError('Cannot generate a valid module name from {}'
                             .format(self.project))
        self.stdout.write('   Module name is "{}"\n'.format(n))
        self.module_name = n

    def get_source_paths(self):
        self.stdout.write('\n** Validating source directories.')
        message = 'Cannot find resource {}'
        for x in [
                  ('manage.py', 'isfile', 'managepy'),
                  ('s13core', 'isdir', 's13coredir'),
                  ('website', 'isdir', 'websitedir')
                ]:
            p = os.path.join(self.source, x[0])
            if x[1] == 'isfile':
                if not os.path.isfile(p):
                    raise IOError(message.format(p))
            else:
                if not os.path.isdir(p):
                    raise IOError(message.format(p))
            setattr(self, x[2], p)

    def make_project_dir(self):
        self.stdout.write('** Cloning S13Core from source.')
        if os.path.isdir(self.project):
            if not self.is_overwrite:
                raise IOError('Project directory already exists, please' +
                              ' include the --overwrite flag to recreate it.')
            else:
                shutil.rmtree(self.project)
        os.mkdir(self.project)
        shutil.copy(self.managepy, os.path.join(self.project, 'manage.py'))
        shutil.copytree(self.websitedir,
                        os.path.join(self.project, self.module_name))
        os.symlink(self.s13coredir, os.path.join(self.project, 's13core'))
        # Remove the db.sqlite file if it is present.
        if os.path.isfile(os.path.join(self.project, self.module_name,
                                       'db.sqlite3')):
            os.remove(
                os.path.join(self.project, self.module_name, 'db.sqlite3')
            )

    def replace_values(self):
        self.stdout.write('** Tweaking project settings.')
        # Replace the module settings in manage.py.
        with open(os.path.join(self.project, 'manage.py'), 'r+') as f:
            contents = f.read().replace(
                'website.settings.development',
                '{}.settings.development'.format(self.module_name)
            )
            f.seek(0)
            f.write(contents)
            f.truncate()
        # Replace the module settings in wsgi.py.
        with open(os.path.join(
                self.project, self.module_name, 'wsgi.py'), 'r+') as f:
            contents = f.read().replace(
                'website.settings.development',
                '{}.settings.development'.format(self.module_name)
            )
            f.seek(0)
            f.write(contents)
            f.truncate()
        # Replace the secret key, root conf, and wsgi app in settings.py.
        secret_key = self._generate_secret_key(50, 4)
        for fn in ['development.py', 'production.py']:
            with open(os.path.join(
                    self.project, self.module_name,
                    'settings', fn), 'r+') as f:
                contents = f.read()\
                    .replace(s.SECRET_KEY, secret_key)\
                    .replace('website.urls',
                             '{}.urls'.format(self.module_name))\
                    .replace('website.wsgi',
                             '{}.wsgi'.format(self.module_name))
                f.seek(0)
                f.write(contents)
                f.truncate()

    def _generate_secret_key(self, length, repetitions):
        # We could have used a built-in utitlity for this but what the heck...
        characters = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret = ''
        # Want a secret key of @length number of characters.
        while len(secret) < 50:
            selected = choice(characters)
            # We want a maximum repetition of @repetition per character.
            while secret.count(selected) > 4:
                selected = choice(characters)
            secret += selected
        return secret
