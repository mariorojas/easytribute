from django.urls import path

from . import views

app_name = 'tributes'

urlpatterns = [
    path('', views.TributeHomeView.as_view(), name='home'),
    path('dashboard/', views.TributeDashboardView.as_view(), name='dashboard'),
    path('edit/', views.TributeUpdateView.as_view(), name='edit'),
    path('new/', views.TributeCreateView.as_view(), name='new'),
    path('new/anon/', views.TributeCreateAnonymousView.as_view(), name='new-as-anon'),
    path('<slug:slug>/', views.TributeDetailView.as_view(), name='detail'),
    path('<slug:slug>/share/', views.TributeShareView.as_view(), name='share'),
]
