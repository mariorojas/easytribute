from django.urls import path

from .views import delete, flag

urlpatterns = [
    path('delete/<int:comment_id>/', delete, name='comments-delete'),
    path('flag/<int:comment_id>/', flag, name='comments-flag'),
]
