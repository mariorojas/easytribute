# comments

This application can be used to attach comments to any model.

The following features are included:

- All the features in django-contrib-comments
- Comments in descending order

**Installation**

1. Install **django-contrib-comments** according to [this tutorial](https://django-contrib-comments.readthedocs.io/en/latest/quickstart.html)
2. In your project settings.py
   1. Add `comments.apps.CommentsConfig` to INSTALLED_APPS
   2. Add `COMMENTS_APP = 'comments'`
3. In your project urls.py
   1. Insert `path('comments/', include('comments.urls')),` before the URLs definition for **django-contrib-comments**
4. Run `python manage.py migrate` to update your database schema
5. For more information, visit the [django-contrib-comments](https://django-contrib-comments.readthedocs.io/en/latest/index.html) official documentation