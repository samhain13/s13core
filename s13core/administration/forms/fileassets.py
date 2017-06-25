from django import forms

from s13core.content_management.models import FileAsset


class FileAssetForm(forms.ModelForm):
    class Meta:
        model = FileAsset
        exclude = ['extension']

    def __init__(self, *args, **kwargs):
        super(FileAssetForm, self).__init__(*args, **kwargs)
        if self.instance.pk is None:
            self.fields['media_file'].required = True
