from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ChangeInformationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ChangePasswordForm(forms.ModelForm):
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['password']
        widgets = {'password': forms.PasswordInput()}

    def clean(self):
        old_p = self.cleaned_data['password'].strip()
        self.new_p0 = self.cleaned_data['new_password'].strip()
        new_p1 = self.cleaned_data['confirm_password'].strip()
        user = authenticate(username=self.instance.username, password=old_p)
        if user is None:
            raise forms.ValidationError('Invalid current password.')
        if self.new_p0 != new_p1:
            raise forms.ValidationError('New and confirm password mismatch.')

    def save(self):
        self.instance.set_password(self.new_p0)
        self.instance.save()
