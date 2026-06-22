"""
URL configuration for final_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from Social_media import views
from Social_media.views import home, contacts, like_Post, post_detail, post_list, register_view, user_profile, share_post, user_update
#import debug_toolbar.urls
from django.urls import include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('notifications/read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('posts/', post_list, name='post_list'),
    path('posts/<int:pk>/', post_detail, name='post_detail'),
    path('like/<int:pk>/', like_Post.as_view(), name='like_post'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('user/<str:username>/',user_profile, name='user_profile'),
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('comment/edit/<int:pk>/', views.edit_comment, name='edit_comment'),
    path('comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('share/<int:pk>/', share_post, name='share_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('user/<int:pk>/update/', views.user_update.as_view(), name='user_update'),
    path('search/', views.search_users, name='search_users'),
    path('friend/add/<str:username>/', views.add_friend, name='add_friend'),
    path('friend/remove/<str:username>/', views.remove_friend, name='remove_friend'),
    #path('__debug__/', include(debug_toolbar.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

