import os
from django.shortcuts import render
from django.contrib import messages
{% if use_share_links %}
from cryptography.fernet import Fernet
{% endif %}
from django.contrib.auth.decorators import login_required
from quarto.models import (
    AppUser,
    {% if use_share_links %}
    ShareLink,
    ShareLinkUsage,
    {% endif %}{% if use_group_permissions %}
    ProjectGroupPermission,
    Project, {% endif %}
    )

{% if use_social_auth %}
@login_required {% endif %}
def index(request, path=None):
    if not path:
        path = 'index.html'
    if not '.html' in path:
        path = path + 'index.html'

    user = request.user

    # Create Page View Record
    if not user.is_anonymous:
        user.pageview_set.create(content_path=path if path else '')

    {% if use_group_permissions %}
    # Check if the user has Project view permission
    if ProjectGroupPermission.objects.count() > 0:  # This if check can be removed once permissions have been set in the admin panel
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
    {% else %}
    return render(request, f"projects/{path}")
    {% endif %}


{% if use_share_links %}
def share(request):
    if not request.user.is_anonymous:
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
    else:
        return render(request, 'projects/index.html')
{% endif %}

def login(request):
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

{% if use_share_links %}
def decrypt(encryption):
    key = os.environ.get('ENCRYPTION_KEY')
    cipher = Fernet(key)
    return cipher.decrypt(bytes(encryption, 'utf-8')).decode()
{% endif %}