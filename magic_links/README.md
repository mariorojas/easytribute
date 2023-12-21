# magic_links

This application can be used to log in users with email links, also known as magic links.

The following features are included:

- All the features in django-sesame

**Installation**

1. Install **django-sesame** according to [this tutorial](https://django-sesame.readthedocs.io/en/stable/tutorial.html)
2. In your project settings.py
   1. Add `magic_links.apps.MagicLinksConfig` to INSTALLED_APPS
   2. Config the values for `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL`
3. In your project urls.py
   1. Add `path('accounts/', include('magic_links.urls'))`
4. For more information, visit the [django-sesame](https://django-sesame.readthedocs.io/en/stable/index.html) official documentation