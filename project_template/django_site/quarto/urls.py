from django.urls import path
from . import views

urlpatterns = [
    {% if use_share_links %}
    path("share/", views.share),
    {% endif %}
    path("about.html", views.about),
    path("", views.index),
    ]
