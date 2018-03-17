from django import forms

from s13core.socmed_collector.models import APIKey
from s13core.socmed_collector.models import SocMedFeed
from s13core.socmed_collector.models import SocMedProcessor


class APIKeyForm(forms.ModelForm):
    class Meta:
        model = APIKey
        fields = '__all__'


class SocMedFeedForm(forms.ModelForm):
    class Meta:
        model = SocMedFeed
        fields = ['label', 'account_id', 'api_key', 'processor', 'max_results']


class SocMedProcessorForm(forms.ModelForm):
    class Meta:
        model = SocMedProcessor
        fields = '__all__'
