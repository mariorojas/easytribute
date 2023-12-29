from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_comments.admin import CommentsAdmin

from .models import CustomComment, Report


@admin.register(CustomComment)
class CustomCommentAdmin(CommentsAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ['comment_link']

    def comment_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse('admin:comments_customcomment_change', args=(obj.comment.pk,)),
            obj.comment.pk
        ))
