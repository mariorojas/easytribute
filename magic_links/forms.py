from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from . import blacklist


class EmailLoginForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not settings.TEMPORARY_EMAIL_LOGIN:
            domain = email.split('@')[1]
            if domain in blacklist.DOMAINS:
                raise ValidationError(_('Temporary emails are not allowed'))
        return email
