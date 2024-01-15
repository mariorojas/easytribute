from django.urls import path

from .views import to_bruno

app_name = 'to_bruno'

urlpatterns = [
    path('', to_bruno, name='home')
]
