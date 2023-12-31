import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView
from sesame.utils import get_query_string

from .forms import EmailLoginForm

MESSAGE = """Hi,

Sign in to EasyTribute by clicking on the following link:

    {0}

If you did not request this email, you can safely ignore it.
"""

MODERATE_APP = 'django_comments'
MODERATE_PERMISSION = 'can_moderate'
PERMISSION = f'{MODERATE_APP}.{MODERATE_PERMISSION}'


class EmailLoginView(FormView):
    template_name = 'magic_links/email_login.html'
    form_class = EmailLoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        user_model = get_user_model()
        user = user_model.objects.filter(username=email).first()

        if not user:
            raw_password = str(uuid.uuid4())
            user = user_model.objects.create_user(
                username=email,
                email=email,
                password=raw_password,
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
