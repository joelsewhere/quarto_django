from django.urls import path
from . import views

urlpatterns = [
    path("share/", views.share),
    path("about.html", views.about),
    path("", views.index),
    ]
