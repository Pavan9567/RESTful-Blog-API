"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from blogapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.Register.as_view(),name='register_user'),
    path('login/',views.Login.as_view(),name='login_user'),
    path('posts/',views.PostListCreate.as_view(),name='post_list_create'),
    path('posts/<int:pk>/',views.PostRetrieveUpdateDestroy.as_view(),name='post_list_update_delete'),
    path('comments/',views.CommentListCreate.as_view(),name='comment_list_create'),
    path('comments/<int:pk>/',views.CommentRetrieveUpdateDestroy.as_view(),name='comment_list_update_delete'),

    path('',include('blogapp.urls')),

]