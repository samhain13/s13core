from django import forms

from s13core.settings.models import ContactInfo
from s13core.settings.models import CopyrightInfo
from s13core.settings.models import Disclaimer
from s13core.settings.models import Setting


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = '__all__'


class CopyrightInfoForm(forms.ModelForm):
    class Meta:
        model = CopyrightInfo
        fields = '__all__'


class DisclaimerForm(forms.ModelForm):
    class Meta:
        model = Disclaimer
        fields = '__all__'


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = '__all__'
