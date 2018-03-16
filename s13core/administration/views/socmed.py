from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from s13core.socmed_collector.models import APIKey
from s13core.socmed_collector.models import SocMedFeed
from s13core.socmed_collector.models import SocMedProcessor

from ..forms.socmed import APIKeyForm
from ..forms.socmed import SocMedFeedForm
from ..forms.socmed import SocMedProcessorForm
from ..mixins import GenericCRUDMixin
from ..mixins import S13UserRequiredMixin


class SocMedListMixin(S13UserRequiredMixin):
    mode = None
    template_name = 'admin/list_socmed.html'
    ui_description = 'Generic Social Media Collector user interface.'
    ui_title = 'Social Media Collector Mixin'

    def get_context_data(self, **kwargs):
        context = super(SocMedListMixin, self).get_context_data(**kwargs)
        context['mode'] = self.mode
        return context


class SocMedCRUDMixin(GenericCRUDMixin):
    context_sidebars = ['nav_socmed']
    template_name = 'admin/forms/update_socmed.html'


class APIKeyList(SocMedListMixin, ListView):
    mode = 'socmedapikey'
    model = APIKey
    ui_description = '''
    API Keys are used for authentication on other websites like
    Facebook, Twitter, and YouTube. Those websites, in turn, provide access
    to your posts so that they can be re-posted on this website.
    '''
    ui_title = 'Social Media API Keys'


class APIKeyCreate(SocMedCRUDMixin, CreateView):
    context_cancel_url = reverse_lazy('s13admin:socmedapikeys')
    form_class = APIKeyForm
    model = APIKey
    success_message = 'API Key created.'
    success_url = reverse_lazy('s13admin:socmedapikeys')
    ui_description = 'Create a new API Key.'
    ui_title = 'Create API Key'


class APIKeyDelete(SocMedCRUDMixin, DeleteView):
    context_cancel_url = reverse_lazy('s13admin:socmedapikeys')
    model = APIKey
    success_message = 'API Key deleted.'
    success_url = reverse_lazy('s13admin:socmedapikeys')
    template_name = 'admin/delete.html'
    ui_description = 'Are you sure you want to delete this API Key?'
    ui_title = 'Delete API Key'


class APIKeyUpdate(SocMedCRUDMixin, UpdateView):
    context_cancel_url = reverse_lazy('s13admin:socmedapikeys')
    form_class = APIKeyForm
    model = APIKey
    success_message = 'API Key updated.'
    success_url = reverse_lazy('s13admin:socmedapikeys')
    ui_description = 'Update this API Key.'
    ui_title = 'Update API Key'


class SocMedFeedList(SocMedListMixin, ListView):
    mode = 'socmedfeed'
    model = SocMedFeed
    ui_description = '''
    Social Media Feeds represent snapshots of the posts that you have made
    in a registered Social Media website like Facebook and Twitter. Feeds
    need an API Key and Feed Processor, which provide access controls to your
    Social Media and processing instructions for the data response.
    '''
    ui_title = 'Social Media Feeds'


class SocMedFeedCreate(SocMedCRUDMixin, CreateView):
    context_cancel_url = reverse_lazy('s13admin:socmedfeeds')
    form_class = SocMedFeedForm
    model = SocMedFeed
    success_message = 'Social Media Feed created.'
    success_url = reverse_lazy('s13admin:socmedfeeds')
    ui_description = 'Create a new Social Media Feed.'
    ui_title = 'Create Social Media Feed'


class SocMedFeedDelete(SocMedCRUDMixin, DeleteView):
    context_cancel_url = reverse_lazy('s13admin:socmedfeeds')
    model = SocMedFeed
    success_message = 'Social Media Feed deleted.'
    success_url = reverse_lazy('s13admin:socmedfeeds')
    template_name = 'admin/delete.html'
    ui_description = 'Are you sure you want to delete this Feed?'
    ui_title = 'Delete Social Media Feed'


class SocMedFeedUpdate(SocMedCRUDMixin, UpdateView):
    context_cancel_url = reverse_lazy('s13admin:socmedfeeds')
    form_class = SocMedFeedForm
    model = SocMedFeed
    success_message = 'Social Media Feed updated.'
    success_url = reverse_lazy('s13admin:socmedfeeds')
    ui_description = 'Update this Social Media Feed.'
    ui_title = 'Update Social Media Feed'


class SocMedProcessorList(SocMedListMixin, ListView):
    mode = 'socmedprocessor'
    model = SocMedProcessor
    ui_description = '''
    Feed Processors contain processing instructions that are taylored for
    data responses from registered Social Media websites like Facebook and
    Twitter. Feed Processor objects include a Python Code field whose contents
    are <code>eval'ed</code> each time a request for downloading a Social Media
    feed is made. Use this facility with care.
    '''
    ui_title = 'Social Media Processors'


class SocMedProcessorCreate(SocMedCRUDMixin, CreateView):
    context_cancel_url = reverse_lazy('s13admin:socmedprocessors')
    form_class = SocMedProcessorForm
    model = SocMedProcessor
    success_message = 'Social Media Feed Processor created.'
    success_url = reverse_lazy('s13admin:socmedprocessors')
    ui_description = 'Create a new Social Media Feed Processor.'
    ui_title = 'Create Social Media Feed Processor'


class SocMedProcessorDelete(SocMedCRUDMixin, DeleteView):
    context_cancel_url = reverse_lazy('s13admin:socmedprocessors')
    model = SocMedProcessor
    success_message = 'Social Media Feed Processor deleted.'
    success_url = reverse_lazy('s13admin:socmedprocessors')
    template_name = 'admin/delete.html'
    ui_description = 'Are you sure you want to delete this Processor?'
    ui_title = 'Delete Social Media Feed Processor'


class SocMedProcessorUpdate(SocMedCRUDMixin, UpdateView):
    context_cancel_url = reverse_lazy('s13admin:socmedprocessors')
    form_class = SocMedProcessorForm
    model = SocMedProcessor
    success_message = 'Social Media Feed Processor updated.'
    success_url = reverse_lazy('s13admin:socmedprocessors')
    ui_description = 'Update this Social Media Feed Processor.'
    ui_title = 'Update Social Media Feed Processor'


class RetrieveSocMedFeed(SocMedListMixin, DetailView):
    model = SocMedFeed

    def get_context_data(self, **kwargs):
        context = super(RetrieveSocMedFeed, self).get_context_data(**kwargs)
        # Get the JSON first.
        # error = self.object.get_response()
        # if error:
        #     messages.error(self.request, str(error))
        #     return context  # Skip processing.
        # Process the response.
        error = self.object.process_response()
        if error:
            messages.error(self.request, str(error))
            return context
        return context
