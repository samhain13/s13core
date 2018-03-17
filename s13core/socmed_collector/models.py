import json
import os
import urllib.request

from django.conf import settings as s
from django.core.exceptions import FieldError
from django.db import models

from s13core.content_management.models import Article
from s13core.content_management.models import FileAsset


class SocMedModel(models.Model):
    '''Abstract model providing:

    1. label fields are case-insensitively unique
    2. a common __str__ method
    '''
    label = models.CharField(max_length=64, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.label)

    def save(self, *args, **kwargs):
        if hasattr(self.__class__, 'objects'):
            if self.__class__.objects.filter(
                    label__iexact=self.label).exclude(pk=self.pk):
                raise FieldError(
                    'label "{}" is not unique'.format(self.label))
        return super(SocMedModel, self).save(*args, **kwargs)


class APIKey(SocMedModel):
    '''Represents an API key to be used when requesting resources from
    a Social Media website.
    '''
    key = models.CharField(max_length=128, unique=True)
    label = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = 'API Key'


class SocMedProcessor(SocMedModel):
    '''Stores some Python 3 code to be used for processing a downloaded
    resource from a Social Media website using an API Key and account_id.
    '''
    label = models.CharField(max_length=64, unique=True)
    uri = models.CharField(max_length=255, verbose_name='API Endpoint URI')
    code = models.TextField(verbose_name='Python Code')
    notes = models.TextField()

    class Meta:
        verbose_name = 'Social Media Feed Processor'


class SocMedFeed(SocMedModel):
    '''Represents a Social Media account feed and some
    processing instructions.
    '''
    label = models.CharField(max_length=64, unique=True)
    account_id = models.CharField(
        max_length=64,
        verbose_name='Account ID'
    )
    api_key = models.ForeignKey(
        APIKey,
        verbose_name='API Key'
    )
    processor = models.ForeignKey(
        SocMedProcessor,
        verbose_name='Feed Processor'
    )
    max_results = models.IntegerField(default=5)
    response = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Social Media Feed'

    @property
    def response_json(self):
        '''Converts the value of the response field to a dict.'''
        return json.loads(self.response)

    @property
    def uri(self):
        '''Returns a formatted version of the processor's URI.'''

        return self.processor.uri.format(
            api_key=self.api_key.key,
            account_id=self.account_id,
            items=self.max_results
        )

    def get_response(self):
        '''Makes an HTTP request the a social media website and collects
        the response so that the processor can do something with it.
        '''
        try:
            with urllib.request.urlopen(self.uri) as response:
                self.response = response.read()
                self.save()
            return None
        except urllib.error.HTTPError as e:
            return e

    def process_response(self):
        '''Executes a user-provided code snippet that should handle the data
        supplied in the response JSON.
        '''
        try:
            exec(self.processor.code)
            return None
        except Exception as e:
            return e

    def save_as_fileasset(
                self, post_id, file_asset_uri, title=None, description=None):
        '''Saves a resource locally as a FileAsset object (see CMS).'''

        ext = file_asset_uri.split('/')[-1]
        filename = '{}.{}'.format(post_id, ext)
        target_path = os.path.join(s.MEDIA_ROOT, filename)

        # If the target filename already exists in the media directory, that
        # means we have an existing FileAsset for it (ideally). Return that.
        if os.path.isfile(target_path):
            return FileAsset.objects.filter(media_file=target_path).first()

        # If anything goes wrong, just return None so that the parent
        # process can continue.
        try:
            with urllib.request.urlopen(file_asset_uri) as downloaded:
                asset = FileAsset()
                asset.title = title
                asset.description = description
                asset.media_file.save(filename, downloaded, save=True)
                asset.save()
            return asset
        except Exception:
            return None
