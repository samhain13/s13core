from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from s13core.settings.models import ContactInfo
from s13core.settings.models import CopyrightInfo
from s13core.settings.models import Disclaimer
from s13core.settings.models import Setting

from ..forms.settings import ContactInfoForm
from ..forms.settings import CopyrightInfoForm
from ..forms.settings import DisclaimerForm
from ..forms.settings import SettingsForm
from ..mixins import GenericCRUDMixin


class SettingsList(GenericCRUDMixin, ListView):
    template_name = 'admin/list_settings.html'
    model = Setting
    form_class = SettingsForm
    ui_title = 'Website Settings List'
    ui_description = 'View and select website settings for editing ' + \
        'and activation.'
    context_sidebars = ['nav_settings']

    def get_context_data(self, **kwargs):
        context = super(SettingsList, self).get_context_data(**kwargs)
        context['create_mode'] = 'settings'
        return context


class SettingsCreate(GenericCRUDMixin, CreateView):
    template_name = 'admin/forms/update_settings.html'
    model = Setting
    form_class = SettingsForm
    ui_title = 'Create New Settings'
    ui_description = 'Create new settings.'
    success_message = 'Settings created.'
    context_sidebars = ['nav_settings']


class SettingsDelete(GenericCRUDMixin, DeleteView):
    template_name = 'admin/delete.html'
    model = Setting
    form_class = SettingsForm
    ui_title = 'Delete Settings'
    ui_description = 'Delete selected settings. This cannot be undone.'
    success_message = 'Settings deleted.'
    context_sidebars = ['nav_settings']
    context_cancel_url = reverse_lazy('s13admin:settings')


class SettingsUpdate(GenericCRUDMixin, UpdateView):
    template_name = 'admin/forms/update_settings.html'
    model = Setting
    form_class = SettingsForm
    ui_title = 'Update Settings'
    ui_description = 'Update settings values.'
    success_message = 'Settings updated.'
    context_sidebars = ['nav_settings']


class ContactInfoList(GenericCRUDMixin, ListView):
    template_name = 'admin/list_contact_info.html'
    model = ContactInfo
    ui_title = 'Website Contact Information List'
    ui_description = 'View and select website contact information for editing.'
    context_sidebars = ['nav_settings']

    def get_context_data(self, **kwargs):
        context = super(ContactInfoList, self).get_context_data(**kwargs)
        context['create_mode'] = 'contact-info'
        return context


class ContactInfoCreate(GenericCRUDMixin, CreateView):
    template_name = 'admin/forms/update_settings.html'
    model = ContactInfo
    form_class = ContactInfoForm
    ui_title = 'Create New Settings'
    ui_description = 'Create new contact information.'
    success_message = 'Contact information created.'
    success_url = reverse_lazy('s13admin:contact_info')
    context_sidebars = ['nav_settings']


class ContactInfoDelete(GenericCRUDMixin, DeleteView):
    template_name = 'admin/delete.html'
    model = ContactInfo
    ui_title = 'Delete Contact Information'
    ui_description = 'Delete contact information. This cannot be undone.'
    success_message = 'Contact information deleted.'
    success_url = reverse_lazy('s13admin:contact_info')
    context_sidebars = ['nav_settings']
    context_cancel_url = reverse_lazy('s13admin:contact_info')


class ContactInfoUpdate(GenericCRUDMixin, UpdateView):
    template_name = 'admin/forms/update_settings.html'
    model = ContactInfo
    form_class = ContactInfoForm
    ui_title = 'Update Contact Information'
    ui_description = 'Update contact information values.'
    success_message = 'Contact information updated.'
    success_url = reverse_lazy('s13admin:contact_info')
    context_sidebars = ['nav_settings']


class CopyrightInfoList(GenericCRUDMixin, ListView):
    template_name = 'admin/list_copyright_info.html'
    model = CopyrightInfo
    ui_title = 'Website Copyright Information List'
    ui_description = 'View and select website copyright information for ' + \
        'editing.'
    context_sidebars = ['nav_settings']

    def get_context_data(self, **kwargs):
        context = super(CopyrightInfoList, self).get_context_data(**kwargs)
        context['create_mode'] = 'copyright-info'
        return context


class CopyrightInfoCreate(GenericCRUDMixin, CreateView):
    template_name = 'admin/forms/update_settings.html'
    model = CopyrightInfo
    form_class = CopyrightInfoForm
    ui_title = 'Create New Copyright Information'
    ui_description = 'Create new copyright information.'
    success_message = 'Copyright information created.'
    success_url = reverse_lazy('s13admin:copyright_info')
    context_sidebars = ['nav_settings']


class CopyrightInfoDelete(GenericCRUDMixin, DeleteView):
    template_name = 'admin/delete.html'
    model = CopyrightInfo
    ui_title = 'Delete Copyright Information'
    ui_description = 'Delete copyright information. This cannot be undone.'
    success_message = 'Copyright information deleted.'
    success_url = reverse_lazy('s13admin:copyright_info')
    context_sidebars = ['nav_settings']
    context_cancel_url = reverse_lazy('s13admin:copyright_info')


class CopyrightInfoUpdate(GenericCRUDMixin, UpdateView):
    template_name = 'admin/forms/update_settings.html'
    model = CopyrightInfo
    form_class = CopyrightInfoForm
    ui_title = 'Update Copyright Information'
    ui_description = 'Update copyright information values.'
    success_message = 'Copyright information updated.'
    success_url = reverse_lazy('s13admin:copyright_info')
    context_sidebars = ['nav_settings']


class DisclaimerList(GenericCRUDMixin, ListView):
    template_name = 'admin/list_disclaimer.html'
    model = Disclaimer
    ui_title = 'Website Disclaimer List'
    ui_description = 'View and select website disclaimer for editing.'
    context_sidebars = ['nav_settings']

    def get_context_data(self, **kwargs):
        context = super(DisclaimerList, self).get_context_data(**kwargs)
        context['create_mode'] = 'disclaimer'
        return context


class DisclaimerCreate(GenericCRUDMixin, CreateView):
    template_name = 'admin/forms/update_settings.html'
    model = Disclaimer
    form_class = DisclaimerForm
    ui_title = 'Create New Disclaimer'
    ui_description = 'Create new disclaimer.'
    success_message = 'Copyright information created.'
    success_url = reverse_lazy('s13admin:disclaimer')
    context_sidebars = ['nav_settings']


class DisclaimerDelete(GenericCRUDMixin, DeleteView):
    template_name = 'admin/delete.html'
    model = Disclaimer
    ui_title = 'Delete Disclaimer'
    ui_description = 'Delete disclaimer. This cannot be undone.'
    success_message = 'Disclaimer deleted.'
    success_url = reverse_lazy('s13admin:disclaimer')
    context_sidebars = ['nav_settings']
    context_cancel_url = reverse_lazy('s13admin:disclaimer')


class DisclaimerUpdate(GenericCRUDMixin, UpdateView):
    template_name = 'admin/forms/update_settings.html'
    model = Disclaimer
    form_class = DisclaimerForm
    ui_title = 'Update Disclaimer'
    ui_description = 'Update Disclaimer values.'
    success_message = 'Disclaimer updated.'
    success_url = reverse_lazy('s13admin:disclaimer')
    context_sidebars = ['nav_settings']
