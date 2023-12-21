from django_comments.models import Comment


class CustomComment(Comment):
    class Meta(Comment.Meta):
        ordering = ('-submit_date',)
