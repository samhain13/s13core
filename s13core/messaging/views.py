from django.contrib import messages
from django.views.generic import CreateView

from s13core import helpers as h
from s13core.content_management.views import S13CMSMixin
from s13core.settings.models import Setting

from .forms import SiteMessageForm
from .models import SiteMessage


class S13MessagingMixin(S13CMSMixin):

    def dispatch(self, request, *args, **kwargs):
        self.sections = []
        self.articles = []
        self.article = []
        self.settings = Setting.objects.get(is_active=True)
        return super().dispatch(self.request, *self.args, **self.kwargs)


class SiteMessageCreate(S13MessagingMixin, CreateView):
    form_class = SiteMessageForm
    model = SiteMessage
    template_name = 'defaults/site-message.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        for key, message in form.errors.items():
            messages.error(self.request, '{}: {}'.format(message[0], key))
        return super().form_invalid(form)
