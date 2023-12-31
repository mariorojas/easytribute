from django.db import models
from django.utils import timezone
from django_comments.models import Comment


class CustomComment(Comment):
    class Meta(Comment.Meta):
        ordering = ('-submit_date',)


class ReportManager(models.Manager):
    pass


class Report(models.Model):
    SUGGEST_REMOVAL = 'removal suggestion'
    MODERATOR_DELETION = 'moderator deletion'
    MODERATOR_APPROVAL = 'moderator approval'

    comment = models.ForeignKey(
        Comment, verbose_name='comment', related_name='reports',
        on_delete=models.CASCADE,
    )
    flag = models.CharField(max_length=30, db_index=True)
    flag_date = models.DateTimeField(default=None)

    objects = ReportManager()

    class Meta:
        unique_together = [('comment', 'flag')]

    def __str__(self):
        return '%s flag of comment ID %s' % (self.flag, self.comment.pk)

    def save(self, *args, **kwargs):
        if self.flag_date is None:
            self.flag_date = timezone.now()
        super().save(*args, **kwargs)
