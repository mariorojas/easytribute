from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from . import blacklist


class AccountSettingsForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    def save(self, user):
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()


class EmailLoginForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not settings.TEMPORARY_EMAIL_LOGIN:
            domain = email.split('@')[1]
            if domain in blacklist.DOMAINS:
                raise ValidationError('Temporary emails are not allowed')
        return email
