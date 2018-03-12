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
    mode = None
    template_name = 'admin/list_socmed.html'
    title = 'Social Media Collector Mixin'

    def get_context_data(self, **kwargs):
        context = super(SocMedListMixin, self).get_context_data(**kwargs)
        context['mode'] = self.mode
        context['mode_title'] = self.title
        return context


class APIKeyList(SocMedListMixin, ListView):
    mode = 'apikeys'
    model = APIKey
    title = 'API Keys'


class SocMedFeedList(SocMedListMixin, ListView):
    mode = 'socmedfeed'
    model = SocMedFeed
    title = 'Social Media Feeds'


class SocMedProcessorList(SocMedListMixin, ListView):
    mode = 'socmedfeed'
    model = SocMedProcessor
    title = 'Social Media Processors'
