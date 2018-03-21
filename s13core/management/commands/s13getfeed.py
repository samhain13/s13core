from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.conf import settings as s

from s13core.socmed_collector.models import SocMedFeed


class Command(BaseCommand):
    help = 'Fetches and processes a defined Social Media feed.'

    def add_arguments(self, parser):
        parser.add_argument(
            'feed_label', help='label of a Social Media Feed object'
        )

    def handle(self, *args, **options):
        feed = SocMedFeed.objects.filter(label=options['feed_label']).first()
        if not feed:
            raise CommandError('Feed does not exist!')
        error = feed.get_response()
        if error:
            raise error
        error = feed.process_response()
        if error:
            raise error
        self.stdout.write('** Feed downloaded and processed. Goodbye.')
