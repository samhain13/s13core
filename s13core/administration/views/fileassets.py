from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from s13core.content_management.models import FileAsset

from ..forms.fileassets import FileAssetForm
from ..mixins import GenericCRUDMixin


class FileAssetCRUDMixin(GenericCRUDMixin):
    '''Superclass for views related to Article CRUD operations.'''

    form_class = FileAssetForm
    model = FileAsset
    success_url = reverse_lazy('s13admin:fileassets')
    context_sidebars = ['nav_fileassets']
    paginate_by = 8


class FileAssetsList(FileAssetCRUDMixin, ListView):
    template_name = 'admin/list_files.html'
    ui_title = 'FileAssets List'

    def get(self, request, *args, **kwargs):
        self.q = self.request.GET.get('q', '').strip()
        return super(FileAssetsList, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FileAssetsList, self).get_context_data(**kwargs)
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
        if self.q:
            if self.q.startswith('extension-'):
                return FileAsset.objects.filter(
                    extension__in=self.q.split('-')[-1].split('|')
                )
            else:
                return FileAsset.objects.filter(
                    Q(title__icontains=self.q) |
                    Q(description__icontains=self.q) |
                    Q(alt_text__icontains=self.q)
                )
        else:
            return FileAsset.objects.all()


class FileAssetCreate(FileAssetCRUDMixin, CreateView):
    template_name = 'admin/forms/update_fileasset.html'
    ui_title = 'Create New FileAsset'
    ui_description = 'Upload a media file and create a new FileAsset object.'
    success_message = 'FileAsset created.'


class FileAssetDelete(FileAssetCRUDMixin, DeleteView):
    template_name = 'admin/delete.html'
    ui_title = 'Delete FileAsset'
    ui_description = 'Delete a FileAsset and its associated media file. ' + \
        'This cannot be undone.'
    success_message = 'FileAsset deleted.'
    context_delete_text = 'Delete FileAsset'


class FileAssetUpdate(FileAssetCRUDMixin, UpdateView):
    template_name = 'admin/forms/update_fileasset.html'
    ui_title = 'Update FileAsset'
    ui_description = 'Upload a new media file and/or update an existing ' + \
        'FileAsset object\' information.'
    success_message = 'FileAsset updated.'
