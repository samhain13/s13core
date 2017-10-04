'''General helpers for all s13core submodules.'''

import os
from markdown import markdown

from django.apps import apps
from django.conf import settings as s
from django.utils import timezone


def format_date(date, with_time=False):
    '''Generates a formatted date based on a datetime object.

    Arguments:
        date - datetime object
        with_time - boolean; if True, include the time
    '''
    f = '%d %B %Y'
    if with_time:
        f = '{} {}'.format(f, '%H:%M:%S')
    return date.strftime(f)


def get_contact_info(contact_name):
    '''Returns a ContactInfo instance based on contact_name. If multiple
    objects are selectable, the last instance based on weight is returned.
    '''
    ContactInfo = apps.get_model('settings', 'ContactInfo')
    info = ContactInfo.objects.filter(contact_name=contact_name).last()
    if not info:
        return ContactInfo()
    return info


def get_latest_articles(limit=12):
    '''Returns a selection of the latest Article objects (excluding sections).
    Typically used by templates with customized content selection.
    '''
    Article = apps.get_model('content_management', 'Article')
    return Article.objects.filter(is_public=True).exclude(
        parent=None).order_by('-pk')[:limit]


def get_now():
    '''Generates a timezone-aware datetime object.'''

    return timezone.now()


def is_current_section(current_article, section_slug):
    '''Evaluates the current article and determines whether it falls under
    the section with the given slug. Returns True or False.
    '''
    if not current_article:  # Probably due to a 404 error.
        return False
    current_section = current_article.get_section() \
        if current_article.parent else current_article
    return current_section.slug == section_slug


def make_nav_items(articles, current_url='/', classes=''):
    '''Returns a list of navigation items as HTML anchors.

    Arguments:
        articles - an iterable containing Article model instances
        current_url - serves as a comparison value for determining whether
            a generated link will have the "active" class
        classes - optional CSS classes for each link generated
    '''
    items = []
    for item in articles:
        item_url = item.make_url()
        css_classes = ' class="{}{}{}"'.format(
            'active' if item_url == current_url else '',
            ' ' if item_url == current_url and classes else '',
            classes
        )
        if css_classes == ' class=""':
            css_classes = ''
        items.append('<a href="{}"{}>{}</a>'.format(item_url, css_classes,
                     'Home' if item.is_homepage else item.title))
    return items


def make_paginator_nav(
        page, base_url, prev_text='Previous', next_text='Next',
        nav_id=None, classes=''):
    '''Returns a nav element with class "paginator-nav" containing previous
    and next links, as well as other information.

    Arguments:
        page - a Paginator instance
        base_url - the URL where the GET parameter will be appended
        prev_text - text value for the back/previous page link
        next_text - text value for the next page link
        nav_id - optional ID for the nav element to be created
        classes - optional, additional classes for the nav element
    '''
    nav = '<nav'
    if nav_id:
        nav += ' id="{}" '.format(nav_id)
    nav += ' class="paginator-nav'
    if classes:
        nav += ' {}'.format(classes)
    nav += '">'
    if page.has_previous():
        nav += '<a href="{}{}" rel="prev">{}</a>'.format(
            base_url,
            '?p={}'.format(page.previous_page_number())
            if page.previous_page_number() > 1 else '',
            prev_text
        )
    else:
        nav += '<span class="prev">{}</span>'.format(prev_text)
    nav += '<span class="middle">Page {} of {}</span>'.format(
        page.number, page.paginator.num_pages
    )
    if page.has_next():
        nav += '<a href="{}?p={}" rel="next">{}</a>'.format(
            base_url,
            page.next_page_number(),
            next_text
        )
    else:
        nav += '<span class="next">{}</span>'.format(next_text)
    nav += '</nav>\n'
    return nav


def make_slug_from_date(date):
    '''Generates a slug based on a datetime object.

    Arguments:
        date - datetime object
    '''
    return date.strftime('%Y%m%d-%H%M%S')


def make_template_choices(more_extensions=[]):
    '''Generates a choices tuple for template fields in models.'''

    extensions = ['.html', '.xml', '.json', '.atom'] + more_extensions
    choices = []
    prefix = os.path.join(s.BASE_DIR, 'templates') + os.sep
    # Too deep, but what can we do?
    for td in s.TEMPLATES:
        for d in td['DIRS']:
            for path, directories, files in os.walk(d):
                if not path.endswith('defaults') and not \
                        path.endswith('admin') and not \
                        path.endswith('admin/sidebars') and not \
                        path.endswith('admin/forms') and not \
                        path.endswith('testers'):
                    for f in files:
                        filename, file_extension = os.path.splitext(f)
                        if file_extension in extensions and \
                                not f.startswith('_'):
                            name = os.path.join(path, f).replace(prefix, '')
                            choices.append([name, name])
    return choices


def make_tabs(text, tabs=1):
    '''Adds tabs to text for HTML formatting.'''

    return text.replace('\n', '\n{}'.format('    ' * tabs))


def static(path_to_file):
    '''Prepends the STATIC_URL from settings to the given path.'''

    return '{}{}'.format(s.STATIC_URL, path_to_file)
