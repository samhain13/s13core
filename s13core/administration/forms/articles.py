from django import forms

from s13core import helpers as h
from s13core.content_management.models import Article


class ArticleForm(forms.ModelForm):
    template = forms.ChoiceField(
        required=False,
        choices=[['', '------------']] + h.make_template_choices()
    )

    class Meta:
        model = Article
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['media'].required = False

    def get_fields(self, field_names):
        return [self[x] for x in field_names]
