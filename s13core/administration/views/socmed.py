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
    description = '''
    API Keys are used for authentication on other websites like
    Facebook, Twitter, and YouTube. Those websites, in turn, provide access
    to your posts so that they can be re-posted on this website.
    '''
    mode = 'socmedapikey'
    model = APIKey
    title = 'Social Media API Keys'


class APIKeyCreate(SocMedCRUDMixin, CreateView):
    description = 'Create a new API Key.'
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
    description = 'Update this API Key.'
    form_class = APIKeyForm
    model = APIKey
    success_message = 'API Key updated.'
    success_url = reverse_lazy('s13admin:socmedapikeys')
    title = 'Update API Key'


class SocMedFeedList(SocMedListMixin, ListView):
    description = '''
    Social Media Feeds represent snapshots of the posts that you have made
    in a registered Social Media website like Facebook and Twitter. Feeds
    need an API Key and Feed Processor, which provide access controls to your
    Social Media and processing instructions for the data response.
    '''
    mode = 'socmedfeed'
    model = SocMedFeed
    title = 'Social Media Feeds'


class SocMedFeedCreate(SocMedCRUDMixin, CreateView):
    description = 'Create a new Social Media Feed.'
    form_class = SocMedFeedForm
    model = SocMedFeed
    success_message = 'Social Media Feed created.'
    success_url = reverse_lazy('s13admin:socmedfeeds')
    title = 'Create Social Media Feed'


class SocMedFeedDelete(SocMedCRUDMixin, DeleteView):
    cancel_url = reverse_lazy('s13admin:socmedfeeds')
    description = 'Are you sure you want to delete this Feed?'
    model = SocMedFeed
    success_message = 'Social Media Feed deleted.'
    success_url = reverse_lazy('s13admin:socmedfeeds')
    template_name = 'admin/delete.html'
    title = 'Delete Social Media Feed'

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(SocMedFeedDelete, self).post(
            self.request, *self.args, **self.kwargs)


class SocMedFeedUpdate(SocMedCRUDMixin, UpdateView):
    description = 'Update this Social Media Feed.'
    form_class = SocMedFeedForm
    model = SocMedFeed
    success_message = 'Social Media Feed updated.'
    success_url = reverse_lazy('s13admin:socmedfeeds')
    title = 'Update Social Media Feed'


class SocMedProcessorList(SocMedListMixin, ListView):
    description = '''
    Feed Processors contain processing instructions that are taylored for
    data responses from registered Social Media websites like Facebook and
    Twitter. Feed Processor objects include a Python Code field whose contents
    are <code>eval'ed</code> each time a request for downloading a Social Media
    feed is made. Use this facility with care.
    '''
    mode = 'socmedprocessor'
    model = SocMedProcessor
    title = 'Social Media Processors'


class SocMedProcessorCreate(SocMedCRUDMixin, CreateView):
    description = 'Create a new Social Media Feed Processor.'
    form_class = SocMedProcessorForm
    model = SocMedProcessor
    success_message = 'Social Media Feed Processor created.'
    success_url = reverse_lazy('s13admin:socmedprocessors')
    title = 'Create Social Media Feed Processor'


class SocMedProcessorDelete(SocMedCRUDMixin, DeleteView):
    cancel_url = reverse_lazy('s13admin:socmedapikeys')
    description = 'Are you sure you want to delete this Processor?'
    model = SocMedProcessor
    success_message = 'Social Media Feed Processor deleted.'
    success_url = reverse_lazy('s13admin:socmedprocessors')
    template_name = 'admin/delete.html'
    title = 'Delete Social Media Feed Processor'

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(SocMedProcessorDelete, self).post(
            self.request, *self.args, **self.kwargs)


class SocMedProcessorUpdate(SocMedCRUDMixin, UpdateView):
    description = 'Update this Social Media Feed Processor.'
    form_class = SocMedProcessorForm
    model = SocMedProcessor
    success_message = 'Social Media Feed Processor updated.'
    success_url = reverse_lazy('s13admin:socmedprocessors')
    title = 'Update Social Media Feed Processor'
