"""
URL configuration for django_spotify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from rankings import views

urlpatterns = [
    path("artists_ranking/", views.artists_ranking),
    path("tracks_ranking/", views.tracks_ranking),
    path("artists_ranking_details/", views.artists_ranking_details),
    path("tracks_ranking_details/", views.tracks_ranking_details),
]
