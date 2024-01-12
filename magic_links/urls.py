from django.contrib.auth import views as auth_views
from django.urls import path
from sesame import views as sesame_views

from . import views

app_name = 'magic_links'

urlpatterns = [
    path('auth/', sesame_views.LoginView.as_view(), name='auth'),
    path('login/', views.EmailLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/', views.AccountSettingsView.as_view(), name='settings'),
    path('<int:pk>/detail/', views.AccountDetailView.as_view(), name='detail'),
]
