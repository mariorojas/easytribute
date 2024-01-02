from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django_comments import signals, get_model

from django_comments.views import comments, moderation
from django_comments.views.utils import next_redirect

from comments.models import Report


@csrf_protect
@require_POST
def post_comment(request, next=None, using=None):
    real_ip = request.META.get('HTTP_X_REAL_IP', None)
    if real_ip:
        request.META['REMOTE_ADDR'] = real_ip
    return comments.post_comment(request, next, using)


@csrf_protect
@login_required
@permission_required('django_comments.can_moderate', raise_exception=True)
def delete(request, comment_id, next=None):
    site = get_current_site(request)
    comment = get_object_or_404(get_model(), pk=comment_id, site__pk=site.pk)
    owner = comment.content_object.owner
    if request.user.username != owner:
        raise PermissionDenied()
    return moderation.delete(request, comment_id, next)


@csrf_protect
def flag(request, comment_id, next=None):
    site = get_current_site(request)
    comment = get_object_or_404(get_model(), pk=comment_id, site__pk=site.pk)

    if request.method == 'POST':
        perform_flag(request, comment)
        fallback = next or 'comments-flag-done'
        return next_redirect(request, fallback=fallback, c=comment.pk)

    context = {'comment': comment, 'next': next}
    return render(request, 'comments/flag.html', context)


def perform_flag(request, comment):
    flag_, created = Report.objects.get_or_create(
        comment=comment, flag=Report.SUGGEST_REMOVAL
    )

    print(f'Comment {comment.pk} was flagged by anon user at {flag_.flag_date}')

    if created:
        signals.comment_was_flagged.send(
            sender=comment.__class__,
            comment=comment,
            flag=flag_,
            created=created,
            request=request,
        )
