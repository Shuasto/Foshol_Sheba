from django.urls import path
from . import views

app_name = "farmers"

urlpatterns = [
    path('dashboard/', views.farmer_dashboard, name='dashboard'),
    path('diagnose/', views.diagnose_crop, name='diagnose_crop'),
    path('diagnose/result/<int:pk>/', views.diagnostic_result, name='diagnostic_result'),
    path('diagnose/history/', views.diagnostic_history, name='diagnostic_history'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('diagnose/result/<int:pk>/pdf/', views.export_diagnosis_pdf, name='export_diagnosis_pdf'),
]
