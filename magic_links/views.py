import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from sesame.utils import get_query_string

from .forms import AccountSettingsForm, EmailLoginForm

MESSAGE = """Hi,

Sign in to EasyTribute by clicking on the following link:

    {0}

If you did not request this email, you can safely ignore it.
"""

MODERATE_APP = 'django_comments'
MODERATE_PERMISSION = 'can_moderate'
PERMISSION = f'{MODERATE_APP}.{MODERATE_PERMISSION}'


class AccountSettingsView(LoginRequiredMixin, FormView):
    template_name = 'magic_links/account_settings.html'
    form_class = AccountSettingsForm
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial.update({
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
        return initial
    
    def form_valid(self, form):
        form.save(self.request.user)
        return super().form_valid(form)

    def get_redirect_field_name(self):
        return None


class EmailLoginView(FormView):
    template_name = 'magic_links/email_login.html'
    form_class = EmailLoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        user_model = get_user_model()
        user = user_model.objects.filter(username=email).first()

        if not user:
            raw_password = str(uuid.uuid4())
            random_str = str(uuid.uuid4())[:6]
            user = user_model.objects.create_user(
                username=email,
                email=email,
                password=raw_password,
                first_name='User',
                last_name=random_str
            )

        if not user.has_perm(PERMISSION):
            permission = Permission.objects.get_by_natural_key(
                codename=MODERATE_PERMISSION,
                app_label=MODERATE_APP,
                model='comment',
            )
            user.user_permissions.add(permission)

        link = self.request.build_absolute_uri(reverse('magic_links:auth'))
        link += get_query_string(user)

        user.email_user(
            subject='Sign In to EasyTribute',
            message=MESSAGE.format(link),
            from_email=settings.EMAIL_HOST_USER,
        )

        return render(self.request, 'magic_links/email_login_success.html')
