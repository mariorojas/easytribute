import random
import string

from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit
from django import forms
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django_recaptcha.fields import ReCaptchaField

from .models import Tribute
from .utils import restricted_slugs

user_comment = _("On behalf EasyTribute, we extend our sincere condolences. "
                 "May fond memories bring comfort during this time.")
user_email = 'support@easytribute.com'
user_name = 'EasyTribute team'


class TributeForm(forms.ModelForm):
    slug = forms.SlugField(label='URL')

    class Meta:
        model = Tribute
        fields = ['name', 'description', 'birth_year', 'death_year', 'slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('name', 'description', 'birth_year', 'death_year',
                PrependedText('slug', settings.BASE_SITE_URL)),
            Submit('submit', _('Save changes'), css_class='btn btn-dark'),
        )

    def clean_death_year(self):
        birth_year = self.cleaned_data.get('birth_year')
        death_year = self.cleaned_data.get('death_year')
        if birth_year and birth_year > death_year:
            raise ValidationError(
                _('The death year cannot be lower than the birth year'))
        return death_year

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug in restricted_slugs:
            raise ValidationError(
                _('%(value)s is not allowed'),
                params={'value': slug})
        return slug


class NewTributeForm(forms.ModelForm):
    class Meta:
        model = Tribute
        fields = ['name', 'description', 'birth_year', 'death_year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('name', 'description', 'birth_year', 'death_year'),
            Submit('submit', _('Create'), css_class='btn btn-dark'),
        )

    def save_with_comments(self, user, site_id, ip_address):
        create_slug = True
        while create_slug:
            slug = "".join([random.choice(string.ascii_lowercase) for _ in range(6)])
            if slug in restricted_slugs:
                continue

            tribute_from_db = Tribute.objects.filter(slug=slug)
            if tribute_from_db.exists():
                continue

            self.instance.slug = slug

            if user.is_authenticated:
                self.instance.owner = user

            create_slug = False

        # tribute is saved
        self.instance = super().save()

        # default comment is saved
        custom_comment_model = apps.get_model('comments', 'CustomComment')
        comment = custom_comment_model(
            content_object=self.instance, user_name=user_name, user_email=user_email,
            comment=user_comment, is_public=True, ip_address=ip_address,
            site_id=site_id)
        comment.save()

        return self.instance

    def clean_death_year(self):
        birth_year = self.cleaned_data.get('birth_year')
        death_year = self.cleaned_data.get('death_year')
        if birth_year and birth_year > death_year:
            raise ValidationError(
                _('The death year cannot be lower than the birth year'))
        return death_year


class AnonymousTributeForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Tribute
        fields = ['name', 'description', 'birth_year', 'death_year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('name', 'description', 'birth_year', 'death_year', 'captcha'),
            Submit('submit', _('Create'), css_class='btn btn-dark'),
        )

    def save_with_comments(self, user, site_id, ip_address):
        create_slug = True
        while create_slug:
            slug = "".join([random.choice(string.ascii_lowercase) for _ in range(6)])
            if slug in restricted_slugs:
                continue

            tribute_from_db = Tribute.objects.filter(slug=slug)
            if tribute_from_db.exists():
                continue

            self.instance.slug = slug

            if user.is_authenticated:
                self.instance.owner = user

            create_slug = False

        # tribute is saved
        self.instance = super().save()

        # default comment is saved
        custom_comment_model = apps.get_model('comments', 'CustomComment')
        comment = custom_comment_model(
            content_object=self.instance, user_name=user_name, user_email=user_email,
            comment=user_comment, is_public=True, ip_address=ip_address,
            site_id=site_id)
        comment.save()

        return self.instance

    def clean_death_year(self):
        birth_year = self.cleaned_data.get('birth_year')
        death_year = self.cleaned_data.get('death_year')
        if birth_year and birth_year > death_year:
            raise ValidationError(
                _('The death year cannot be lower than the birth year'))
        return death_year
