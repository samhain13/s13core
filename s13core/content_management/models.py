import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from jinja2 import Template

import s13core
from s13core import helpers as h


DATE_FORMAT = '%A, %d %B %Y - %H:%M'


class ArticleManager(models.Manager):
    def get_homepage(self):
        '''Selects the homepage of the website.'''

        return self._select_by_filter(is_homepage=True, is_public=True)

    def get_section(self, section_slug):
        '''Selects a "section" by its slug; a "section" is simply an Article
        that has no parent.
        '''
        return self._select_by_filter(slug=section_slug, parent=None)

    def get_sections(self):
        '''Selects and sorts the website's sections by weight.'''

        sections = []
        selection = self._select_by_filter(return_all=True, parent=None)
        if not selection:
            return sections
        for section in selection.order_by('-is_homepage', 'weight'):
            section.pre_render()
            sections.append(section)
        return sections

    def get_article(self, section_slug, article_slug):
        '''Selects an Article; validates that it does indeed fall under a
        section with the given slug. Returns both the section and the Article.
        '''
        article = self._select_by_filter(slug=article_slug)
        if not article:
            return None, None
        if article.parent is None:
            return None, None
        section = article.get_section()
        if section.slug != section_slug:
            return None, None
        return section, article

    def _select_by_filter(self, **kwargs):
        '''Multi-model selector for finding sub-classed Articles.'''
        # If return_all is included in kwargs, don't return just one item
        # but return the whole selecttion (see get_sections).
        return_all = "return_all" in kwargs
        if return_all:
            return_all = kwargs['return_all'] is True
            del kwargs['return_all']
        s = Article.objects.filter(**kwargs)
        if not s:
            return None
        if return_all:
            return s
        else:
            s[0].pre_render()
            return s[0]


class Article(models.Model):
    '''An Article is the basic unti of content in an S13Core website.'''

    objects = ArticleManager()
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text='Leave blank to allow the system to auto-generate.'
    )
    owner = models.ForeignKey(User, default=1)
    title = models.CharField(
        max_length=255,
        null=True,
        help_text='HTML compliance is recommended; i.e. use ' +
                  '&amp;amp; for &amp;\'s.'
    )
    body = models.TextField(
        null=True,
        blank=True,
        help_text='Usually HTML but may vary depending on the template. ' +
                  'May also contain Jinja2 code.'
    )

    # Meta information.
    description = models.CharField(max_length=255, null=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
    date_made = models.DateTimeField(null=True, blank=True)
    date_edit = models.DateTimeField(auto_now=True, null=True)

    # Article relationships.
    image = models.ForeignKey(
        'FileAsset',
        null=True,
        blank=True,
        help_text='Associate an image with this article.',
        related_name='article_image'
    )
    parent = models.ForeignKey(
        'Article',
        null=True,
        blank=True,
        help_text='Assiciate this article as a child of another article.'
    )
    sidelinks = models.ManyToManyField(
        'Article',
        blank=True,
        related_name='side_links'
    )
    media = models.ManyToManyField(
        'FileAsset',
        blank=True,
        related_name='article_media',
        help_text='Associate file assets like photos to this article.'
    )
    sort_article_media = models.CharField(
        choices=[
            ('title', 'Title Ascending'),
            ('-title', 'Title Descending'),
            ('alt_text', 'Alt Text Ascending'),
            ('-alt_text', 'Alt Text Descending'),
        ],
        max_length=128,
        default='title',
        blank=True,
        help_text='Sorting strategy for media associated with this article.'
    )

    # Display-related fields.
    template = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    js = models.TextField(
        null=True,
        blank=True,
        verbose_name='JavaScript',
        help_text='Custom JavaScript for this article.'
    )
    css = models.TextField(
        null=True,
        blank=True,
        verbose_name='Custom CSS',
        help_text='Custom Cascading Style Sheet for this article.'
    )
    is_public = models.BooleanField(
        default=True,
        help_text='Make this article available to your viewers.'
    )
    is_homepage = models.BooleanField(
        default=False,
        help_text='Make this article the website\'s homepage.'
    )
    sort_children = models.CharField(
        max_length=255,
        choices=[
            ('pk', 'Date Made (Oldest First)'),
            ('-pk', 'Date Made (Newest First)'),
            ('date_edit', 'Edit Date (Freshest First)'),
            ('-date_edit', 'Edit Date (Freshest Last)'),
            ('title', 'Title (Alphabetical)'),
            ('-title', 'Title (Reverse Alphabetical)'),
            ('weight', 'Weight (Ascending)'),
            ('-weight', 'Weight (Descending)'),
        ],
        blank=True,
        default='-pk',
        help_text='Sorting strategy for child articles when generating<br />' +
                  'navigation links and other user interfaces.'
    )
    include_children = models.IntegerField(
        default=0,
        blank=True,
        help_text='Number of child articles to include in a page;<br />' +
                  'i.e., a Paginator instance.'
    )
    weight = models.IntegerField(
        default=0,
        blank=True,
        help_text='Use this field as an alternate sorting value.'
    )

    def __str__(self):
        return self.title

    @property
    def date_edit_text(self):
        return self.date_edit.strftime(DATE_FORMAT)

    @property
    def date_made_text(self):
        return self.date_made.strftime(DATE_FORMAT)

    def get_ancestry(self, ancestors=None):
        '''Returns a list of an Article's ancestors.'''

        if ancestors is None:
            ancestors = []
        if self.parent:
            ancestors.append(self.parent)
            return self.parent.get_ancestry(ancestors)
        return ancestors

    def get_children(self, exclude_private=True):
        '''Returns a list of Articles whose parent is the current one.'''

        if exclude_private:
            return list(Article.objects.filter(parent=self, is_public=True)
                        .order_by(self.sort_children))
        else:
            return list(Article.objects.filter(parent=self)
                        .order_by(self.sort_children))

    def get_progeny(self):
        '''Returns a list of an Article's descendants.'''

        # This might be expensive; we leave ourselves open to other options.
        descendants = [x for x in Article.objects.all()
                       if x.get_section() == self]
        return descendants

    def get_section(self):
        '''Returns the Article's oldest ancestor, if any.'''

        ancestry = self.get_ancestry()
        return ancestry[-1] if ancestry else None

    def get_siblings(self, exclude_private=True):
        '''Returns a list of Articles whose parent matches the current's parent.
        The list returned includes the current article.
        '''
        # We use weight as default because Articles that have no parent are
        # sections; and sections should be intentionally ordered.
        sorter = self.parent.sort_children if self.parent else 'weight'
        if exclude_private:
            return list(Article.objects.filter(parent=self.parent,
                        is_public=True).order_by(sorter))
        else:
            return list(Article.objects.filter(parent=self.parent)
                        .order_by(sorter))

    def make_url(self):
        '''Generates a URL that is appropriate for this article.'''

        if self.is_homepage:
            return reverse('s13cms:homepage')
        # Between a section and an article.
        if self.parent is None:
            return reverse('s13cms:section', args=[self.slug])
        else:
            return reverse('s13cms:article',
                           args=[self.get_section().slug, self.slug])

    def pre_render(self):
        '''Pre-render the body.'''

        if self.body:
            self.body = Template(self.body).render(s13=s13core, article=self)
        else:
            self.body = ''

    def save(self, *args, **kwargs):
        if self.pk:
            a = Article.objects.get(pk=self.pk)
            if a.date_made.strftime('%Y%m%d%H%M%S') != \
                    self.date_made.strftime('%Y%m%d%H%M%S'):
                raise ValidationError('Creation date is read-only.')
            if a == self.parent:
                raise ValidationError('Article cannot be its own parent.')
        if not self.date_made:
            self.date_made = h.get_now()
        # Generate a slug based on the date if a slug was not given.
        if not self.slug:
            self.slug = h.make_slug_from_date(self.date_made)
        # We want only one homepage.
        if self.is_homepage:
            for a in Article.objects.filter(is_homepage=True):
                a.is_homepage = False
                a.save()
        super(Article, self).save(*args, **kwargs)


class OverwriteStorage(FileSystemStorage):
    # stackoverflow.com/questions/9522759/
    # imagefield-overwrite-image-file-with-same-name
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class FileAsset(models.Model):
    '''A FileAsset is an uploaded file that is saved in the MEDIA_ROOT, that
    has some additional information such as title, description, and alt_text.
    '''
    media_file = models.FileField(
        blank=True,
        default=None,
        storage=OverwriteStorage()
    )
    extension = models.CharField(max_length=8, default='', blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    alt_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Value used for alt attributes in images and other elements.'
    )
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = 'File Asset'

    def delete(self):
        '''When a FileAsset is deleted, delete the associated file as well.'''

        for fa in FileAsset.objects.all():
            if fa.path_on_disk == self.path_on_disk:
                break
        else:
            os.remove(self.path_on_disk)
        super(FileAsset, self).delete()

    @property
    def path_on_disk(self):
        if self.media_file:
            return self.media_file.path
        else:
            return None

    @property
    def url(self):
        if self.media_file:
            return self.media_file.url
        else:
            return None

    def save(self, *args, **kwargs):
        if self.media_file:
            self.extension = self.media_file.path.lower().split('.')[-1]
        return super(FileAsset, self).save(*args, **kwargs)
