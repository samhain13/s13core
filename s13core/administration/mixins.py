from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class S13UserRequiredMixin(LoginRequiredMixin):
    '''Extension of LoginRequiredMixin that defines a few more properties.'''

    login_url = reverse_lazy('s13admin:login')
    ui_title = 'Generic User Interface'
    ui_description = 'S13Core generic user interface.'
    redirect_field_name = None

    def get_context_data(self, **kwargs):
        context = super(S13UserRequiredMixin, self).get_context_data(**kwargs)
        context['ui_title'] = self.ui_title
        context['ui_description'] = self.ui_description
        return context


class GenericCRUDMixin(S13UserRequiredMixin):
    '''Provides handling for generic CRUD operations. Originally written as a
    mixin for Settings CRUD, this may also be used for other models. Just
    override the form_class and model as needed.
    '''
    context_cancel_url = ''
    context_sidebars = []
    form_class = None
    model = None
    success_message = 'Success message.'
    success_url = reverse_lazy('s13admin:settings')
    template_name = None
    ui_title = 'CRUD Interface Title'
    ui_description = 'CRUD interface description.'

    def delete(self, *args, **kwargs):
        try:
            response = super(GenericCRUDMixin, self).delete(*args, **kwargs)
        except Exception as e:
            # Remove any success messages that may have been written.
            storage = messages.get_messages(self.request)
            storage._queued_messages = []
            # Write out an error message.
            response = redirect(self.success_url)
            messages.error(self.request, e.message)
        return response

    def form_invalid(self, form):
        for key, message in form.errors.items():
            messages.error(self.request, '{}: {}'.format(message[0], key))
        return super(GenericCRUDMixin, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(GenericCRUDMixin, self).get_context_data(**kwargs)
        for k in [x for x in dir(self) if x.startswith('context_')]:
            key = k.replace('context_', '')
            context[key] = getattr(self, k)
        return context

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.success_url
