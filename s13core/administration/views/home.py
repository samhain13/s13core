from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView

from s13core.content_management.models import Article
from s13core.content_management.models import FileAsset
from s13core.helpers import convert_bytes

from ..forms.home import ChangeInformationForm
from ..forms.home import ChangePasswordForm
from ..forms.home import LoginForm
from ..mixins import S13UserRequiredMixin


class Dashboard(S13UserRequiredMixin, TemplateView):
    template_name = 'admin/home.html'
    ui_title = 'Dashboard'
    ui_description = 'Shows some interesting information about the website.'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['change_information_form'] = ChangeInformationForm(
            instance=self.request.user)
        context['change_password_form'] = ChangePasswordForm()
        context['stats'] = self._get_stats()
        return context

    def _get_stats(self):
        s = {}
        # Article statistics.
        articles = Article.objects.all()
        s['articles_count'] = articles.exclude(parent=None).count()
        s['articles_draft'] = articles.filter(
            is_public=False).exclude(parent=None).count()
        s['articles_public'] = s['articles_count'] - s['articles_draft']
        s['sections'] = []
        for section in Article.objects.get_sections():
            num_descendants = len(section.get_progeny())
            if num_descendants:
                pct_all = int((num_descendants / s['articles_count']) * 100)
            else:
                pct_all = 0
            s['sections'].append({
                'title': section.title,
                'num_descendants': num_descendants,
                'pct_all': pct_all
            })
        s['sections_count'] = len(s['sections'])

        # FileAsset statistics.
        s['asset_types'] = {'unknown': {'count': 0, 'size': 0}}
        s['assets_broken'] = 0
        s['assets_total'] = 0
        s['assets_total_size'] = 0
        for fa in FileAsset.objects.all():
            s['assets_total'] += 1
            ext = fa.extension if fa.extension else 'unknown'
            if ext not in s['asset_types']:
                s['asset_types'][ext] = {'count': 0, 'size': 0}
            s['asset_types'][ext]['count'] += 1
            if fa.on_disk:
                size = fa.size
                s['asset_types'][ext]['size'] += size
                s['assets_total_size'] += size
            else:
                s['assets_broken'] += 1
        for k, v in s['asset_types'].items():
            v['pct_all'] = int((v['count'] / s['assets_total']) * 100)
            v['pct_size'] = int((v['size'] / s['assets_total_size']) * 100)
            v['size'] = '{0:.2f}MB'.format(convert_bytes(v['size'], 'mb'))
        # Finally.
        s['assets_total_size'] = '{0:.2f}MB'.format(
            convert_bytes(s['assets_total_size'], 'mb'))
        return s


class UpdatePassword(S13UserRequiredMixin, UpdateView):
    template_name = 'admin/forms/generic.html'
    form_class = ChangePasswordForm
    model = User

    def get(self, request, *args, **kwargs):
        # We want the user to use the form in the dashboard.
        return redirect(reverse('s13admin:dashboard'))

    def get_context_data(self, **kwargs):
        context = super(UpdatePassword, self).get_context_data(**kwargs)
        context['ui_title'] = 'Change Password'
        context['ui_description'] = 'Change the password for this account.'
        return context

    def form_invalid(self, form):
        messages.error(self.request, form.errors['__all__'][0])
        return redirect(reverse('s13admin:dashboard'))

    def get_success_url(self):
        messages.success(self.request, 'Password changed.')
        return reverse_lazy('s13admin:dashboard')


class UpdateUserInformation(S13UserRequiredMixin, UpdateView):
    template_name = 'admin/forms/generic.html'
    form_class = ChangeInformationForm
    model = User

    def get(self, request, *args, **kwargs):
        # We want the user to use the form in the dashboard.
        return redirect(reverse('s13admin:dashboard'))

    def get_context_data(self, **kwargs):
        context = super(UpdateUserInformation, self).get_context_data(**kwargs)
        context['ui_title'] = 'Change User Information'
        context['ui_description'] = \
            'Change the basic information about this user.'
        return context

    def get_success_url(self):
        messages.success(self.request, 'User information changed.')
        return reverse_lazy('s13admin:dashboard')


class Login(FormView):
    template_name = 'admin/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('s13admin:dashboard')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('s13admin:dashboard'))
        return super(Login, self).get(
            self.request, *self.args, **self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        context['ui_title'] = 'Login'
        context['ui_description'] = 'Log in to S13Core website management.'
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return self.form_invalid(form)
        login(self.request, user)
        messages.success(self.request, 'Welcome back, {}!'.format(username))
        return super(Login, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username and/or password.')
        return super(Login, self).form_invalid(form)


class Logout(S13UserRequiredMixin, RedirectView):
    pattern_name = 's13admin:login'

    def get_redirect_url(self, *args, **kwargs):
        messages.success(self.request, 'Thank you for using S13Core. Goodbye.')
        logout(self.request)
        return super(Logout, self).get_redirect_url(*self.args, **self.kwargs)
