from django.contrib import admin
from django_comments.admin import CommentsAdmin

from .models import CustomComment


@admin.register(CustomComment)
class CustomCommentAdmin(CommentsAdmin):
    pass
