from django.urls import path
from django.contrib.auth.views import LogoutView
from experts.views import review_diagnosis
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/expert/', views.expert_dashboard, name='expert_dashboard'),
    path('dashboard/expert/review/<int:pk>/', review_diagnosis, name='review_diagnosis'),
    path('dashboard/company/', views.company_dashboard, name='company_dashboard'),
    
    # Market & Community
    path('market/prices/', views.market_prices, name='marketprice_full_view'),
    path('forum/', views.forum_list, name='forum_list'),
    path('forum/my-posts/', views.my_forum_posts, name='my_forum_posts'),
    path('forum/<int:pk>/', views.forum_detail, name='forum_detail'),
    path('forum/new/', views.forum_create, name='forum_create'),
    
    # Products
    path('products/', views.product_list, name='product_list'),

    # Experts Directory
    path('experts/', views.expert_directory, name='expert_directory'),

    # Crops & Diseases
    path('crops/', views.crop_list, name='crop_list'),
    path('crops/<int:pk>/', views.crop_detail, name='crop_detail'),
    path('diseases/', views.disease_list, name='disease_list'),
    path('diseases/<int:pk>/', views.disease_detail, name='disease_detail'),
]
