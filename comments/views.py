import django_comments
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django_comments import signals

from django_comments.views import moderation
from django_comments.views.utils import next_redirect

from comments.models import Report


@csrf_protect
@login_required
@permission_required("django_comments.can_moderate", raise_exception=True)
def delete(request, comment_id, next=None):
    comment = get_object_or_404(django_comments.get_model(),
                                pk=comment_id,
                                site__pk=get_current_site(request).pk)
    owner = comment.content_object.owner
    if request.user.username != owner:
        raise PermissionDenied()
    return moderation.delete(request, comment_id, next)


@csrf_protect
def flag(request, comment_id, next=None):
    comment = get_object_or_404(django_comments.get_model(),
                                pk=comment_id,
                                site__pk=get_current_site(request).pk)

    if request.method == 'POST':
        perform_flag(request, comment)
        return next_redirect(request, fallback=next or 'comments-flag-done',
                             c=comment.pk)

    else:
        return render(request, 'comments/flag.html', {'comment': comment, "next": next})


def perform_flag(request, comment):
    _flag, created = Report.objects.get_or_create(
        comment=comment,
        flag=Report.SUGGEST_REMOVAL
    )

    print(f'Comment {comment.pk} was flagged by anon user at {_flag.flag_date}')

    if created:
        signals.comment_was_flagged.send(
            sender=comment.__class__,
            comment=comment,
            flag=_flag,
            created=created,
            request=request,
        )
