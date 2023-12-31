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
    list_display = ['report', 'flag_date', 'is_removed']
    readonly_fields = ['comment_link', 'is_removed']

    @admin.display()
    def comment_link(self, obj):
        change_comment_link = reverse(
            viewname='admin:comments_customcomment_change',
            args=[obj.comment.pk],
        )
        link = '<a href="{}">{}</a>'.format(change_comment_link, obj.comment.pk)
        return mark_safe(link)

    @admin.display(boolean=True)
    def is_removed(self, ojb):
        return ojb.comment.is_removed

    @admin.display(description='Report')
    def report(self, obj):
        return obj
