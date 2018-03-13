from django import forms

from s13core.content_management.models import Article
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
        fields = ['label', 'account_id', 'api_key', 'processor', 'cms_section']

    def __init__(self, *args, **kwargs):
        super(SocMedFeedForm, self).__init__(*args, **kwargs)
        self.fields['cms_section'].choices = [
            (x.pk, x.title) for x in Article.objects.get_sections()
        ]


class SocMedProcessorForm(forms.ModelForm):
    class Meta:
        model = SocMedProcessor
        fields = '__all__'
