import os
from django.shortcuts import render
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from quarto.models import (
    AppUser,
    
    )


def index(request, path=None):
    if not path:
        path = 'index.html'
    if not '.html' in path:
        path = path + 'index.html'

    user = request.user

    # Create Page View Record
    if not user.is_anonymous:
        user.pageview_set.create(content_path=path if path else '')

    
    return render(request, f"projects/{path}")
    




def login(request):
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

