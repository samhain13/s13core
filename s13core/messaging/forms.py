from django import forms

from .models import SiteMessage


class SiteMessageForm(forms.ModelForm):
    class Meta:
        model = SiteMessage
        exclude = ['date_sent', 'is_sent']
