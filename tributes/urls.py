from django.urls import path

from . import views

app_name = 'tributes'

urlpatterns = [
    path('', views.TributeHomeView.as_view(), name='home'),
    path('edit/', views.TributeUpdateView.as_view(), name='edit'),
    path('new/', views.TributeCreateView.as_view(), name='new'),
    path('<slug:slug>/', views.TributeDetailView.as_view(), name='detail'),
]
