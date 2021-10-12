from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from s13core.content_management.models import FileAsset
from s13core.content_management.models import Article

from ..forms.articles import ArticleForm
from ..mixins import GenericCRUDMixin
from ..mixins import S13UserRequiredMixin


class ArticlesCRUDMixin(GenericCRUDMixin):
    '''Superclass for views related to Article CRUD operations.'''

    form_class = ArticleForm
    model = Article
    success_url = reverse_lazy('s13admin:articles')
    context_sidebars = ['nav_articles']
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(ArticlesCRUDMixin, self).get_context_data(**kwargs)
        context['sections'] = Article.objects.get_sections()
        return context


class ArticlesList(ArticlesCRUDMixin, ListView):
    '''Articles list and CMS homepage. Allows for searching articles and
    returns paginated results.
    '''
    template_name = 'admin/list_articles.html'
    ui_title = 'Articles List'
    ui_description = 'List of articles that make up the website.'
    context_search_mode = 'all'

    def get(self, request, *args, **kwargs):
        self.q = self.request.GET.get('q', '').strip()
        self.article = None
        if 'pk' in self.kwargs:
            try:
                self.article = Article.objects.get(pk=self.kwargs['pk'])
                self.context_cancel_url = reverse_lazy(
                    's13admin:detail_article', args=[self.kwargs['pk']])
                reverse_args = [self.article.pk]
                if 'mode' in self.kwargs:
                    self.context_search_mode = self.kwargs['mode']
                    self.ui_title = 'Article {}'.format(
                        self.kwargs['mode'].title())
                    reverse_args.append(self.kwargs['mode'])
                self.success_url = reverse_lazy(
                    's13admin:detail_article', args=reverse_args)
            except ObjectDoesNotExist:
                messages.error(self.request, 'Article does not exist.')
        return super(ArticlesList, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticlesList, self).get_context_data(**kwargs)
        context['article'] = self.article
        terms = urlencode({'q': self.q})[2:]
        context['search_terms'] = self.q
        # Paginate search results.
        context['back_link'] = '#search-form'
        context['next_link'] = '#search-form'
        if context['page_obj'].has_previous():
            context['back_link'] = '{}?page={}'.format(
                self.success_url, context['page_obj'].previous_page_number()
            )
            if self.q:
                context['back_link'] += '&q='.format(terms)
        if context['page_obj'].has_next():
            context['next_link'] = '{}?page={}'.format(
                self.success_url, context['page_obj'].next_page_number()
            )
            if self.q:
                context['next_link'] += '&q='.format(terms)
        return context

    def get_queryset(self):
        # Selection depends on what mode the user is on.
        mode = self.kwargs['mode'] if 'mode' in self.kwargs else None
        if self.q:
            pk = self.kwargs['pk'] if 'pk' in self.kwargs else '0'
            if mode == 'image':
                return FileAsset.objects.filter(
                    Q(title__icontains=self.q) |
                    Q(description__icontains=self.q) |
                    Q(alt_text__icontains=self.q)
                ).filter(extension__in=['gif', 'jpg', 'jpeg', 'png', 'svg'])
            elif mode == 'media':
                return FileAsset.objects.filter(
                    Q(title__icontains=self.q) |
                    Q(description__icontains=self.q) |
                    Q(alt_text__icontains=self.q)
                )
            else:
                return Article.objects.filter(
                    Q(slug__icontains=self.q) | Q(title__icontains=self.q) |
                    Q(description__icontains=self.q)
                ).exclude(pk=pk).order_by('-date_edit')
        else:
            # If we have no reference article, just return a selection of
            # the latest articles in the database.
            if not self.article:
                return Article.objects.all().order_by('-date_edit')
            if mode == 'sidelinks':
                return self.article.sidelinks.all()
            elif mode == 'image':
                # Because our interface expects an iterable, we need to put
                # the article's image in a list.
                if self.article.image:
                    return [self.article.image]
                else:
                    return []
            elif mode == 'media':
                return self.article.media.all()
            else:  # children is the default mode.
                return Article.objects.filter(parent=self.article)


class ArticleDetail(ArticlesList):
    '''Shows article details. Accepts a <mode> kwarg which shows the selected
    article's children or sidelinks and allows the user to associate search
    results with the current article.
    '''
    ui_title = 'Article Details'
    ui_description = 'Article details and a list of articles or media ' + \
        'associated with it.'
    context_search_mode = 'children'


class ArticleAssociate(S13UserRequiredMixin, RedirectView):
    '''Does the actual associations and dissociations of parent-children
    and article-sidelinks.
    '''
    def get_redirect_url(self, *args, **kwargs):
        if self.kwargs['action'] not in ['add', 'remove']:
            messages.error(self.request, 'Invalid action specified.')
            return reverse_lazy('s13admin:articles')

        message = 'Article associdated.'
        is_add = self.kwargs['action'] == 'add'
        mode = self.kwargs['mode']
        args = [self.kwargs['pk'], mode]

        try:
            base_article = Article.objects.get(pk=self.kwargs['pk'])
            if mode in ['image', 'media']:
                selected_article = FileAsset.objects.get(pk=self.kwargs['xpk'])
            else:
                selected_article = Article.objects.get(pk=self.kwargs['xpk'])
        except ObjectDoesNotExist:
            messages.error(self.request, 'Article does not exist.')
            return reverse_lazy('s13admin:articles')

        if mode == 'children':
            if is_add:
                selected_article.parent = base_article
                selected_article.save()
                message = 'Article added to child articles.'
            else:
                selected_article.parent = None
                selected_article.save()
                message = 'Article removed from child articles.'
        elif mode == 'image':
            if is_add:
                base_article.image = selected_article
                base_article.save()
                message = 'FileAsset set as Article preview image.'
            else:
                base_article.image = None
                base_article.save()
                message = 'FileAsset unset as Article preview image.'
        elif mode == 'media':
            if is_add:
                base_article.media.add(selected_article)
                message = 'FileAsset added to Article media files.'
            else:
                base_article.media.remove(selected_article)
                message = 'FileAsset removed from Article media files.'
        elif mode == 'sidelinks':
            if is_add:
                base_article.sidelinks.add(selected_article)
                message = 'Article added to sidelinks.'
            else:
                base_article.sidelinks.remove(selected_article)
                message = 'Article removed from sidelinks.'

        messages.success(self.request, message)
        return reverse_lazy('s13admin:detail_article', args=args)


class ArticleCreate(ArticlesCRUDMixin, CreateView):
    '''Shows the create article/section form.'''

    template_name = 'admin/forms/update_article.html'
    ui_title = 'Create New Article'
    ui_description = 'Create new article.'
    success_message = 'Article created.'

    def get_context_data(self, **kwargs):
        context = super(ArticleCreate, self).get_context_data(**kwargs)
        context['parent_pk'] = self.kwargs.get('parent_pk', '')
        return context


class ArticleDelete(ArticlesCRUDMixin, DeleteView):
    '''Shows a delete confirmation page and actually deletes an article.'''

    template_name = 'admin/delete.html'
    ui_title = 'Delete Article'
    ui_description = 'Delete selected article. This cannot be undone.'
    success_message = 'Article deleted.'
    context_delete_text = 'Delete Article'


class ArticleUpdate(ArticlesCRUDMixin, UpdateView):
    '''Shows the update article/section form.'''

    template_name = 'admin/forms/update_article.html'
    ui_title = 'Update Article'
    ui_description = 'Update article values.'
    success_message = 'Article updated.'

    def get_success_url(self):
        self.success_url = reverse_lazy(
            's13admin:detail_article', args=[self.object.pk])
        return super(ArticleUpdate, self).get_success_url()
