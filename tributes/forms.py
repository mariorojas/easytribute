import random
import string

from django import forms
from django.apps import apps
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import Tribute
from .utils import restricted_slugs

user_comment = _("On behalf EasyTribute, we extend our sincere condolences. "
                 "May fond memories bring comfort during this time.")
user_email = 'support@easytribute.com'
user_name = 'EasyTribute team'


class TributeForm(forms.ModelForm):
    slug = forms.SlugField(
        help_text='This value is used to determine your URL. '
                  'For example, if you set your slug to "john-doe", '
                  'your URL will be "https://www.easytribute.com/john-doe".')

    class Meta:
        model = Tribute
        fields = ['name', 'description', 'birth_year', 'death_year', 'slug']

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
                _('The slug %(value)s is not allowed'),
                params={'value': slug})
        return slug


class NewTributeForm(forms.ModelForm):
    class Meta:
        model = Tribute
        fields = ['name', 'description', 'birth_year', 'death_year']

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

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug in restricted_slugs:
            raise ValidationError(
                _('The slug %(value)s is not allowed'),
                params={'value': slug})
        return slug
