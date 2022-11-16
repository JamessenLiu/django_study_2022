"""django_study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from apps.users.views import get_userinfo, get_users, UsersView, \
    UserLoginView, UserArticleView, AticleView, UsersExportView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('userinfo', get_userinfo),
    # path('api/users', get_users),
    path('api/users', UsersView.as_view()),
    path('api/login', UserLoginView.as_view()),
    path('api/users/<int:user_id>/articles', UserArticleView.as_view()),
    path('api/articles', AticleView.as_view()),
    path('api/users/export', UsersExportView.as_view())

]
