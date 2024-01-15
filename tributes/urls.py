from django.urls import path

from . import views

app_name = 'tributes'

urlpatterns = [
    path('dashboard/', views.TributeDashboardView.as_view(), name='dashboard'),
    path('new/', views.TributeCreateView.as_view(), name='new'),
    path('new/anon/', views.AnonymousTributeCreateView.as_view(), name='new-as-anon'),
    path('<slug:slug>/', views.TributeDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', views.TributeUpdateView.as_view(), name='edit'),
    path(
        '<slug:slug>/picture/edit/',
        views.TributePictureUpdateView.as_view(),
        name='edit-picture'
    ),
    path('<slug:slug>/report/', views.ReportCreateView.as_view(), name='new-report'),
    path('<slug:slug>/share/', views.TributeShareView.as_view(), name='share'),
]
