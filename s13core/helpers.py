'''General helpers for all s13core submodules.'''

# Flake8 will complain about a couple of imports but those are needed by
# jinja2env and used by the templates.
import os
import pytz
from markdown import markdown

from django.conf import settings as s
from django.utils import timezone


def convert_bytes(bytes, unit='kb'):
    '''Converts a given number of bytes into different unit values.

    Arguments:
        bytes - integer
        unit - string: bits, kb, mb, gb; default is kb
    '''
    if unit == 'bits':
        return bytes * 8
    elif unit == 'kb':
        return bytes / 1024
    elif unit == 'mb':
        return bytes / 1048576
    elif unit == 'gb':
        return bytes / 1073741824
    else:
        return bytes


def format_date(date, with_time=False):
    '''Generates a formatted date based on a datetime object.

    Arguments:
        date - datetime object
        with_time - boolean; if True, include the time
    '''
    date = date.astimezone(pytz.timezone(s.TIME_ZONE))
    f = '%d %B %Y'
    if with_time:
        f = '{} - {}'.format(f, '%H:%M')
    return date.strftime(f)


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


def make_external_link(href, link_html, item_classes=None, item_id=None):
    '''Convenience function; creates an anchor with rel="noopener noreferrer"
    and target="_blank. Should be marked 'safe' in the template.".
    '''
    if type(item_classes) in [list, tuple]:
        item_classes = ' class="{}"'.format(' '.join(item_classes))
    else:
        item_classes = ''
    if item_id:
        item_id = ' id="{}"'.format(item_id)
    else:
        item_id = ''
    a = '<a href="{}" target="_blank" rel="noopener noreferrer"{}{}>{}</a>'
    return a.format(href, item_classes, item_id, link_html)


def make_nav_items(
            articles, current_url='/', classes='', use_slugs=False,
            include_private=False):
    '''Returns a list of navigation items as HTML anchors.

    Arguments:
        articles - an iterable containing Article model instances
        current_url - serves as a comparison value for determining whether
            a generated link will have the "active" class
        classes - optional CSS classes for each link generated
        use_slugs - if set to True, render the article's slug instead of
            the title
    '''
    items = []
    for item in articles:
        if item.is_public or (item.is_public == False and include_private):
            item_url = item.make_url()
            css_classes = ' class="{}{}{}"'.format(
                'active' if item_url == current_url else '',
                ' ' if item_url == current_url and classes else '',
                classes
            )
            if css_classes == ' class=""':
                css_classes = ''
            link_text = item.slug if use_slugs else item.title
            if item.is_homepage:
                link_text = 'Home'
            items.append('<a href="{}"{}><span>{}</span></a>'.format(
                item_url, css_classes, link_text))
    return items


def make_paginator_nav(
        page, base_url, prev_text='Previous', next_text='Next',
        nav_id=None, classes='', extra_args=''):
    '''Returns a nav element with class "paginator-nav" containing previous
    and next links, as well as other information.

    Arguments:
        page - a Paginator instance
        base_url - the URL where the GET parameter will be appended
        prev_text - text value for the back/previous page link
        next_text - text value for the next page link
        nav_id - optional ID for the nav element to be created
        classes - optional, additional classes for the nav element
        extra_args - optional, additional URL parameters like &amp;q=terms
    '''
    nav = '<nav'
    if nav_id:
        nav += ' id="{}" '.format(nav_id)
    nav += ' class="paginator-nav'
    if classes:
        nav += ' {}'.format(classes)
    nav += '">'
    if page.has_previous():
        prev_link = base_url
        if page.previous_page_number() > 1:
            prev_link += '?p={}'.format(page.previous_page_number())
            if extra_args:
                prev_link += extra_args
        else:
            if extra_args:
                # We're expecting prev_link to start with `&amp;`.
                prev_link += '?{}'.format(extra_args[5:])
        nav += '<a href="{}" rel="prev">{}</a>'.format(prev_link, prev_text)
    else:
        nav += '<span class="prev">{}</span>'.format(prev_text)
    nav += '<span class="middle">Page {} of {}</span>'.format(
        page.number, page.paginator.num_pages
    )
    if page.has_next():
        nav += '<a href="{}?p={}{}" rel="next">{}</a>'.format(
            base_url,
            page.next_page_number(),
            extra_args,
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

    if text is None:
        return ''
    return text.replace('\n', '\n{}'.format('    ' * tabs))


def make_video_iframe(source, classes=None, _id=None, add_referer=False):
    '''Creates a div containing an iframe for embedded videos. Can actually
    be used for iframes containing things other than videos but the function
    was made for embedding YouTube videos.

    Arguments:
        source - URI of the iframe source
        classes - a list of CSS classes for the container div
        _id - optional, a CSS id for the container div (not the iframe)
        add_referer - optional, removes referrerpolicy="no-referrer" if True
    '''
    if type(classes) in [list, tuple]:
        classes.insert('video-iframe', 0)
    else:
        classes = ['video-iframe']
    item_id = 'id="{}" '.format(_id) if _id else ''
    referer_policy = '' if add_referer else ' referrerpolicy="no-referrer"'
    div = '<div {}class="{}"><iframe src="{}"{}></iframe></div>'
    return div.format(item_id, ' '.join(classes), source, referer_policy)


def static(path_to_file):
    '''Prepends the STATIC_URL from settings to the given path.'''

    return '{}{}'.format(s.STATIC_URL, path_to_file)
