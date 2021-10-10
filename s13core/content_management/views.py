from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView

from s13core import helpers as h
from s13core.settings.models import Setting

from .models import Article


class S13CMSMixin(object):
    def get_context_data(self, **kwargs):
        context = super(S13CMSMixin, self).get_context_data(**kwargs)
        context['sections'] = self.sections
        context['articles'] = self.articles
        context['article'] = self.article
        context['s'] = self.settings
        return context

    def get_page_number(self):
        '''Checks whether a page number argument "?p=" was passed and
        whether its value can actually be used as a page number. Returns the
        number on success, None on failure.
        '''
        p = self.request.GET.get('p', '')
        if p == '':
            return None
        return int(p) if p.isdigit() and p != '1' else False

    def paginate_children(self, selection=None, num_pages=0):
        '''Paginates the selected Article's children according to its settings.
        Returns one of two things: a Paginator instance on success;
        None if a "?p=" argument given is invalid.

        @selection and @num_pages are provided by the KeywordSearchView because
        that view is not really based on an article, so there is nothing to
        provide values for those arguments internally.
        '''
        if not selection:
            selection = self.article.get_children()
        if not num_pages:
            if self.article.include_children:
                num_pages = self.article.include_children
            else:
                return None
        p = Paginator(selection, num_pages)
        page_num = self.get_page_number()
        if type(page_num) is int:
            if p.num_pages < page_num or page_num < 1:
                return None
            else:
                return p.page(page_num)
        else:
            if page_num is None:
                return p.page(1)
            else:
                return None

    def get_template(self):
        '''Ensures that the given template can be accessed for rendering.'''

        templates = [x[0] for x in h.make_template_choices()]
        candidate = self.article.template
        return candidate if candidate in templates else self.template_name

    def not_found(self, context):
        return render(self.request, 'defaults/_404.html', context, status=404)

    def tweak_settings(self, view_name):
        '''Modifies some settings values, taking into consideration the
        current view and article content.
        '''
        # Do not save the settings_obj, we just need values for this instance!
        # Tweak the window title.
        if view_name == 'SectionView':
            self.settings.window_title = '{} | {}'.format(
                self.article.title, self.settings.title
            )
        elif view_name == 'ArticleView':
            self.settings.window_title = '{} ({}) | {}'.format(
                self.article.title, self.section.title, self.settings.title
            )
        elif view_name == 'KeywordSearchView':
            self.settings.window_title = 'Keyword Search Results'
        else:
            self.settings.window_title = self.settings.title
        # Take note of the current URL so we can pass it around the view.
        self.settings.current_url = self.article.make_url()
        # Override the description.
        self.settings.description = self.article.description
        # Append website keywords if desired.
        if self.settings.append_keywords:
            self.settings.keywords = '{}, {}'.format(
                self.article.keywords, self.settings.keywords
            )
        # Include any head CSS and JavaScripts from the article.
        if self.article.css:
            self.settings.css += '\n{}'.format(self.article.css)
        if self.article.js:
            self.settings.js += '\n{}'.format(self.article.js)


class HomepageView(S13CMSMixin, TemplateView):
    '''Responds with the website's assigned home page (article). If no article
    has been assigned, a default page is rendered.
    '''
    template_name = 'defaults/homepage.html'

    def get(self, request, *args, **kwargs):
        self.settings = Setting.objects.get(is_active=True)
        self.sections = Article.objects.get_sections()
        self.article = Article.objects.get_homepage()
        # No designated homepage:
        if not self.article:
            # This is not included in the settings model so we need
            # to supply it on the fly.
            self.settings.window_title = self.settings.title
            # If the site is set to display paginated contents when there
            # is no designated homepage, pull the contents from the database.
            if self.settings.nohome_content_type == 'articles':
                self.articles = self.get_paginator(
                    request,
                    Article.objects.exclude(parent=None).order_by('-pk'),
                    self.settings.nohome_content_items
                )
                if self.articles is None:
                    return self.not_found({'s': self.settings})
            else:
                self.articles = []
            self.template_name = 'defaults/no-homepage.html'
            return super(HomepageView, self).get(request, *args, **kwargs)
        # A homepage was designated:
        self.articles = self.paginate_children()
        self.tweak_settings(self.__class__.__name__)
        self.template_name = self.get_template()
        return super(HomepageView, self).get(
            self.request, *self.args, **self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.filter(is_public=True)\
            .exclude(parent=None).exclude(parent=self.article)\
            .order_by('-date_made')[:32]
        return context


class SectionView(S13CMSMixin, TemplateView):
    '''Responds with an Article that has no given parent.'''

    template_name = 'defaults/section.html'

    def get(self, request, *args, **kwargs):
        self.settings = Setting.objects.get(is_active=True)
        self.sections = Article.objects.get_sections()
        self.article = Article.objects.get_section(kwargs['section_slug'])
        # The Section requested is invalid.
        if not self.article:
            return self.not_found({'s': self.settings})
        # Don't show private sections.
        if not self.article.is_public and not \
                self.request.user.is_authenticated():
            return self.not_found({'s': self.settings})
        # The Section requested is valid.
        self.articles = self.paginate_children()
        self.tweak_settings(self.__class__.__name__)
        self.template_name = self.get_template()
        return super(SectionView, self).get(
            self.request, *self.args, **self.kwargs)


class KeywordSearchView(S13CMSMixin, TemplateView):
    '''Resonds with a Search Results page.'''

    template_name = 'defaults/keyword-search.html'

    def get(self, request, *args, **kwargs):
        self.settings = Setting.objects.get(is_active=True)
        self.sections = Article.objects.get_sections()
        self.article = Article(
            slug='keyword-search',
            title='Keyword Search Results',
            body='',
            description='Keyword search results page.',
            keywords='keywords search results'
        )
        terms = request.GET.get('q', None)
        if not terms:
            selection = []
        else:
            selection = Article.objects.search(terms)
        self.articles = self.paginate_children(
            selection, self.settings.keywords_search_items)
        self.tweak_settings(self.__class__.__name__)
        self.template_name = self.get_template()
        return super(KeywordSearchView, self).get(
            self.request, *self.args, **self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(KeywordSearchView, self).get_context_data(**kwargs)
        context['terms'] = self.request.GET.get('q', '')
        return context


class ArticleView(S13CMSMixin, TemplateView):
    '''Responds with an Article that has a given parent.'''

    template_name = 'defaults/article.html'

    def get(self, request, *args, **kwargs):
        self.settings = Setting.objects.get(is_active=True)
        self.sections = Article.objects.get_sections()
        self.section, self.article = Article.objects.get_article(
            kwargs['section_slug'], kwargs['article_slug']
        )
        # The requested Article is invalid.
        if not self.article:
            return self.not_found({'s': self.settings})
        # Don't show private articles or public articles in private sections.
        if not self.request.user.is_authenticated:
            if not self.article.is_public or not self.section.is_public:
                return self.not_found({'s': self.settings})
        # The requested Article is valid.
        self.articles = self.paginate_children()
        self.tweak_settings(self.__class__.__name__)
        self.template_name = self.get_template()
        return super(ArticleView, self).get(
            self.request, *self.args, **self.kwargs)

    def get_context_data(self, **kwargs):
        # The Article's section needs to be passed into the context.
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['section'] = self.section
        context['previous_article'], context['next_article'] = \
            self.article.get_previous_and_next()
        return context


class UITestView(TemplateView):
    '''When settings.DEBUG is True, responds with a context-less template from
    [website]/templates/testers. Use this view when in development as a means
    to test HTML, CSS, and JavaScript.
    '''
    template_name = 'testers/index.html'

    def get(self, request, *args, **kwargs):
        if 'page' in kwargs:
            page = h.os.path.join(h.s.TEMPLATES[0]['DIRS'][0], kwargs['page'])
            if not h.os.path.isfile(page):
                raise Http404('Test page does not exist.')
            self.template_name = 'testers/{}'.format(kwargs['page'])
        return super(UITestView, self).get(
            self.request, *self.args, **self.kwargs)
