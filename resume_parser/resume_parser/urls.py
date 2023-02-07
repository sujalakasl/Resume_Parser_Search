"""resume_parser URL Configuration

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
from django.urls import path, include
from parser_app import views as v
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/", v.register, name="register"),
    path('', include('parser_app.urls')),
    path('', include("django.contrib.auth.urls")),
    path('homepage/Check', v.table, name='table'),
    path('base/logout', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('homepage/search-db', v.search_db, name='search-db'),
    path('', v.homepage, name='homepage'),
    
]
