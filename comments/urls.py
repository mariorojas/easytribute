from django.urls import path

from .views import delete, flag, post_comment

urlpatterns = [
    path('post/', post_comment, name='comments-post-comment'),
    path('delete/<int:comment_id>/', delete, name='comments-delete'),
    path('flag/<int:comment_id>/', flag, name='comments-flag'),
]
