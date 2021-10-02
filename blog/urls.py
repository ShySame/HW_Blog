from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('posts/', views.PostView.as_view(), name='post_list'),
    path('users/', views.AuthorView.as_view(), name='user_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('userpost/<int:pk>/', views.UserPostView.as_view(), name='userposts'),
    path('posts/update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('help/', views.contact_form, name='help_me')

]
