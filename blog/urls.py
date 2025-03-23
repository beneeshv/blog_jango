from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),
    path('post/<slug:slug>/dislike/', views.dislike_post, name='dislike_post'),
    path('post/<slug:slug>/rate/', views.rate_post, name='rate_post'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register, name='register'),
    path("logout/", views.user_logout, name="logout"),
    path('admin-login/', views.admin_login, name='admin_login'),
]
