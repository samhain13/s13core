import json
import urllib.request

from django.core.exceptions import FieldError
from django.db import models

from s13core.content_management.models import Article


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


class SocMedProcessor(SocMedModel):
    '''Stores some Python 3 code to be used for processing a downloaded
    resource from a Social Media website using an API Key and account_id.
    '''
    label = models.CharField(max_length=64, unique=True)
    uri = models.CharField(max_length=255)
    code = models.TextField()
    notes = models.TextField()


class SocMedFeed(SocMedModel):
    '''Represents a Social Media account feed and some
    processing instructions.
    '''
    label = models.CharField(max_length=64, unique=True)
    api_key = models.ForeignKey(APIKey)
    account_id = models.CharField(max_length=64)
    max_results = models.IntegerField(default=5)
    response = models.TextField()
    cms_section = models.ForeignKey(Article)
    processor = models.ForeignKey(SocMedProcessor)

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
        with urllib.request.urlopen(self.uri) as response:
            self.response = response.read()
            self.save()

    def process_response(self):
        '''Totally unsafe.'''

        exec(self.processor.code)
