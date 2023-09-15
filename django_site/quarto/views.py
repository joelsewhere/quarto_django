import os
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from cryptography.fernet import Fernet
from django.contrib.auth.decorators import login_required
from quarto.models import AppUser, ShareLink, ShareLinkUsage, ProjectGroupPermission, Project


@login_required if settings.use_group_permissions else None
def index(request, path=None):
    if not path:
        path = 'index.html'
    if not '.html' in path:
        path = path + 'index.html'

    user = request.user

    # Create Page View Record
    user.pageview_set.create(content_path=path if path else '')

    if settings.use_group_permissions:
        # Check if the user has Project view permission
        project_name = path.split('/')[0]
        if Project.objects.filter(name=project_name).exists():
            project = Project.objects.get(name=project_name)
            permissions = ProjectGroupPermission.objects.get(project=project)
            for group in permissions.group.all():
                if user.groups.filter(name=group.name).exists():
                    return render(request, f"projects/{path}")
            
            # Send user to homepage
            messages.warning(request, 'You do not have permission to view this page.')
            return render(request, "projects/index.html")
        return render(request, "projects/index.html")
    else:
        return render(request, f"projects/{path}")

# This view is only necessary if you have activated 
# the `Copy Share Button!` feature
def share(request):
    # Get shareid and owner_id
    id = request.GET.get('id')
    owner_id = request.GET.get('owner_id')
    # Get owner of the share link
    owner = AppUser.objects.get(email=decrypt(owner_id))
    # Get the url path for the content
    content_path = decrypt(id)
    # Get or create the sharelink record
        # The record does not exist until its first usage
    share_link, created = ShareLink.objects.get_or_create(
        share_id=id,
        user=owner,
        content_path=content_path)
    
    # Update the usage record
    usage, created = ShareLinkUsage.objects.get_or_create(
        user=request.user,
        owner=owner,
        share_link=share_link,
    )
    usage.access_events += 1
    usage.save()

    # Generate page view record
    content_path = usage.share_link.content_path
    request.user.pageview_set.create(content_path=content_path, share_link=share_link)

    return render(request, content_path[1:] + 'index.html')

def login(request):
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def decrypt(encryption):
    key = os.environ.get('ENCRYPTION_KEY')
    cipher = Fernet(key)
    return cipher.decrypt(bytes(encryption, 'utf-8')).decode()