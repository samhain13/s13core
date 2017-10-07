from django.core.exceptions import ValidationError
from django.db import models

from jinja2 import Template

import s13core
from s13core import helpers as h


class Setting(models.Model):
    # Basic Settings
    is_active = models.BooleanField(default=False)
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Setting Name',
        help_text='Unique name for this setting.'
    )
    title = models.CharField(
        max_length=128,
        verbose_name='Website Title',
        help_text='Overall title of the website.',
        default='My S13Core Website'
    )
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='General overview for the website. Used when an article ' +
                  'has a blank description field.'
    )
    keywords = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Keywords associated with the whole website.'
    )
    append_keywords = models.BooleanField(
        default=True,
        help_text='Always append the website keywords to meta information?'
    )
    # No homepage section settings.
    nohome_content_type = models.CharField(
        max_length=12,
        default='none',
        help_text='Show these contents when there is no selected homepage.',
        choices=(
            ('sections', 'Show the website sections'),
            ('articles', 'Show the latest articles'),
            ('custom_html', 'Show a custom html'),
            ('none', 'Show nothing'),
        ),
        verbose_name='Show Contents',
        blank=True
    )
    nohome_content_items = models.IntegerField(
        default=8,
        blank=True,
        help_text='Number of items to show, if any.',
        verbose_name='Items'
    )
    keywords_search_items = models.IntegerField(
        default=12,
        blank=True,
        help_text='Number of search results to show per page, if any.',
        verbose_name='Search Results Items'
    )
    nohome_title = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text='Use this title instead of “Website Under Construction”',
        verbose_name='Alternate Title'
    )
    nohome_custom = models.TextField(
        blank=True,
        verbose_name='Custom HTML',
        help_text='HTML code for when “custom page” is selected.'
    )
    # Head Elements
    css = models.TextField(
        null=True,
        blank=True,
        verbose_name='Stylesheets',
        help_text='Link elements to stylesheets and/or style elements with ' +
                  'inline CSS definitions, like:<br />' +
                  '&lt;link rel="stylesheet" ' +
                  'href="/static/css/default.css" /&gt;'
    )
    js = models.TextField(
        null=True,
        blank=True,
        verbose_name='JavaScripts',
        help_text='Script elements with sources or inline JavaScript code, ' +
                  'like:<br />&lt;script ' +
                  'src="/static/js/test.js"&gt;&lt;/script&gt;'
    )
    # Copyright, Contact, and Disclaimer
    copyright = models.ForeignKey(
        'CopyrightInfo',
        null=True,
        blank=True,
        verbose_name='Copyright Infomration'
    )
    contact = models.ManyToManyField(
        'ContactInfo',
        blank=True,
        verbose_name='Contact Information'
    )
    disclaimer = models.ForeignKey('Disclaimer', null=True, blank=True)

    def __str__(self):
        return '{}{}'.format(self.name, ' (active)' if self.is_active else '')

    def delete(self, *args, **kwargs):
        # Always leave one active setting so the website doesn't break.
        if Setting.objects.count() > 1:
            super(Setting, self).delete(*args, **kwargs)
            other_settings = Setting.objects.filter(is_active=True)
            if not other_settings:
                s = Setting.objects.all()[0]
                s.is_active = True
                s.save()
        else:
            raise ValidationError('One active setting is required.')

    def save(self, *args, **kwargs):
        # There must be only one active setting.
        if self.is_active:
            for s in Setting.objects.filter(is_active=True)\
                    .exclude(name=self.name):
                s.is_active = False
                s.save()
        else:
            if Setting.objects.filter(is_active=True).count() < 1:
                self.is_active = True
        super(Setting, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-is_active', 'title']


class ContactInfo(models.Model):
    contact_name = models.CharField(max_length=255, default='Juan de la Cruz')
    address = models.TextField(
        null=True, blank=True, help_text='Physical address. HTML allowed.')
    email = models.CharField(
        max_length=255, null=True, blank=True,
        help_text='Comma-separated email addresses.'
    )
    phone = models.CharField(
        max_length=255, null=True, blank=True,
        help_text='Comma-separated phone numbers.'
    )
    weight = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.contact_name

    @property
    def address_html(self):
        if self.address:
            self.address = Template(self.address).render(s13=s13core)
        else:
            self.address = ''
        return self.address

    class Meta:
        ordering = ['weight', 'contact_name']
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'


class CopyrightInfo(models.Model):
    statement = models.CharField(
        max_length=255,
        default='',
        help_text='Usually appears at the footer of a webpage, like:<br />' +
                  'Copyright &copy; 2016. Your Company Name. ' +
                  'All rights reserved.',
        verbose_name='Copyright Statement'
    )
    license = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Content licensing reference title, like:<br />' +
                  'Creative Commons Attribution Share-Alike ' +
                  'International License',
        verbose_name='Content License'
    )
    link = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Link to the full content license text, if any.<br />' +
                  'https://creativecommons.org/licenses/by-sa/4.0/legalcode',
        verbose_name='Link to License'
    )

    def __str__(self):
        return self.statement

    def make_statement(self):
        if not self.license:
            return self.statement
        if self.link:
            l = '<br /><a href="{}" target="_blank">{}</a>'\
                .format(self.link, self.license)
        else:
            l = '<br />'.format(self.license)
        return '{}{}'.format(self.statement, l)

    class Meta:
        ordering = ['statement']
        verbose_name = 'Copyright Information'
        verbose_name_plural = 'Copyright Information'


class Disclaimer(models.Model):
    title = models.CharField(max_length=255, default='Disclaimer')
    body = models.TextField(help_text='HTML allowed.', default='')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
