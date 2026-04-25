from django.urls import path
from . import views

app_name = "experts"

urlpatterns = [
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('history/', views.review_history, name='review_history'),
]
