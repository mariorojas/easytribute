from django.urls import path

from .views import to_bruno

app_name = 'tobruno'

urlpatterns = [
    path('', to_bruno, name='home')
]
