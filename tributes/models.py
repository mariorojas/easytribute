import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django_comments.moderation import CommentModerator, moderator


def upload_to(instance, filename):
    rnd = uuid.uuid4()
    ext = filename.split('.')[-1]
    return 'pictures/{}.{}'.format(rnd, ext)


class TributeManager(models.Manager):
    pass


class Tribute(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=3000)
    birth_year = models.PositiveIntegerField()
    death_year = models.PositiveIntegerField()
    picture = models.ImageField(
        upload_to=upload_to,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg'])],
        help_text=_(
            'Images must be equal to or less than 5MB. Allowed file types: jpg, jpeg.'
        ),
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    enable_comments = models.BooleanField(default=True)

    objects = TributeManager()

    def __str__(self):
        return f'{self.slug}'

    def get_absolute_url(self):
        return reverse('tributes:detail', kwargs={'slug': self.slug})


class ReportManager(models.Manager):
    pass


class Report(models.Model):
    tribute = models.ForeignKey(Tribute, on_delete=models.CASCADE)
    detail = models.TextField(max_length=3000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ReportManager()


class TributeModerator(CommentModerator):
    email_notification = False
    enable_field = 'enable_comments'


moderator.register(Tribute, TributeModerator)
