import django_comments
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect

from django_comments.views.moderation import delete as django_comments_delete


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
    return django_comments_delete(request, comment_id, next)
