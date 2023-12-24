from django.urls import path

from .views import delete

urlpatterns = [
    path('delete/<int:comment_id>/', delete, name='comments-delete'),
]
