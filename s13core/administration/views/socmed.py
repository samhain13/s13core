from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from s13core.socmed_collector.models import APIKey
from s13core.socmed_collector.models import SocMedFeed
from s13core.socmed_collector.models import SocMedProcessor

from ..forms.socmed import APIKeyForm
from ..forms.socmed import SocMedFeedForm
from ..forms.socmed import SocMedProcessorForm 
from ..mixins import S13UserRequiredMixin


class SocMedListMixin(S13UserRequiredMixin):
    description = 'Generic Social Media Collector user interface.'
    mode = None
    template_name = 'admin/list_socmed.html'
    title = 'Social Media Collector Mixin'

    def get_context_data(self, **kwargs):
        context = super(SocMedListMixin, self).get_context_data(**kwargs)
        context['mode'] = self.mode
        context['ui_title'] = self.title
        context['ui_description'] = self.description
        return context


class SocMedCRUDMixin(S13UserRequiredMixin):
    cancel_url = None
    description = 'Generic Social Media Collector user interface.'
    failure_message = 'CRUD action failed.'
    success_message = 'CRUD action succeeded.'
    template_name = 'admin/forms/update_socmed.html'
    title = 'Social Media Collector CRUD Mixin'

    def get_context_data(self, **kwargs):
        context = super(SocMedCRUDMixin, self).get_context_data(**kwargs)
        context['ui_title'] = self.title
        context['ui_description'] = self.description
        context['cancel_url'] = self.cancel_url
        context['sidebars'] = ['nav_socmed']
        return context

    def form_valid(self, form):
        response = super(SocMedCRUDMixin, self).form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        response = super(SocMedCRUDMixin, self).form_invalid(form)
        messages.error(self.request, self.failure_message)
        return response


class APIKeyList(SocMedListMixin, ListView):
    mode = 'apikey'
    model = APIKey
    title = 'API Keys'


class APIKeyCreate(SocMedCRUDMixin, CreateView):
    form_class = APIKeyForm
    model = APIKey
    success_message = 'API Key created.'
    success_url = reverse_lazy('s13admin:socmedapikeys')
    title = 'Create API Key'


class APIKeyDelete(SocMedCRUDMixin, DeleteView):
    cancel_url = reverse_lazy('s13admin:socmedapikeys')
    description = 'Are you sure you want to delete this API Key?'
    model = APIKey
    success_message = 'API Key deleted.'
    success_url = reverse_lazy('s13admin:socmedapikeys')
    template_name = 'admin/delete.html'
    title = 'Delete API Key'

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(APIKeyDelete, self).post(
            self.request, *self.args, **self.kwargs)


class APIKeyUpdate(SocMedCRUDMixin, UpdateView):
    form_class = APIKeyForm
    model = APIKey
    success_message = 'API Key updated.'
    success_url = reverse_lazy('s13admin:socmedapikeys')
    title = 'Update API Key'


class SocMedFeedList(SocMedListMixin, ListView):
    mode = 'socmedfeed'
    model = SocMedFeed
    title = 'Social Media Feeds'


class SocMedProcessorList(SocMedListMixin, ListView):
    mode = 'socmedprocessor'
    model = SocMedProcessor
    title = 'Social Media Processors'
