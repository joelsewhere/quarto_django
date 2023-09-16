from django.urls import path
from . import views

urlpatterns = [
    
    path("about.html", views.about),
    path("", views.index),
    ]