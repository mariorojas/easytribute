from django.db import models
from django.urls import reverse
from django_comments.moderation import CommentModerator, moderator


class TributeManager(models.Manager):
    pass


class Tribute(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=3000)
    birth_year = models.PositiveIntegerField()
    death_year = models.PositiveIntegerField()
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


class TributeModerator(CommentModerator):
    email_notification = False
    enable_field = 'enable_comments'


moderator.register(Tribute, TributeModerator)
