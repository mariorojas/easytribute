from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView
from sesame.utils import get_query_string

from .forms import EmailLoginForm

message = """Hi,

Sign in to EasyTribute by clicking on the following link:

    {0}

If you did not request this email, you can safely ignore it.
"""


class EmailLoginView(FormView):
    template_name = 'magic_links/email_login.html'
    form_class = EmailLoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=email)
        except user_model.DoesNotExist:
            raw_password = 'hello'
            user = user_model.objects.create_user(username=email, email=email,
                                                  password=raw_password)

        link = reverse('magic_links:auth')
        link = self.request.build_absolute_uri(link)
        link += get_query_string(user)

        user.email_user(subject='[django-sesame] Login to our app',
                        message=message.format(link))

        return render(self.request, 'magic_links/email_login_success.html')
