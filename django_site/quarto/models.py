import os
from cryptography.fernet import Fernet
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import AppUserManager


class AppUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AppUserManager()

    def __str__(self):
        return self.email
    
    def generate_share_link(self, request_path):
        key = os.environ.get('ENCRYPTION_KEY')
        cipher = Fernet(key)
        share_id = cipher._encrypt_from_parts(bytes(request_path, 'utf-8'), 0,b'\xbd\xc0,\x16\x87\xd7G\xb5\xe5\xcc\xdb\xf9\x07\xaf\xa0\xfa').decode()
        owner_id = cipher._encrypt_from_parts(bytes(self.email, 'utf-8'), 0,b'\xbd\xc0,\x16\x87\xd7G\xb5\xe5\xcc\xdb\xf9\x07\xaf\xa0\xfa').decode()
        print(share_id)
        share_link, created = ShareLink.objects.get_or_create(
            user=self,
            content_path=request_path,
            share_id=share_id
            )
        share_link.save()
        return f'http://localhost:8000/share?id={share_id}&owner_id={owner_id}'

    
class ShareLink(models.Model):

    share_id = models.CharField(max_length=444, null=True)
    user = models.ForeignKey(AppUser, null=True, on_delete=models.SET_NULL)
    content_path = models.FilePathField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def decrypt(encryption):
        key = os.environ.get('ENCRYPTION_KEY')
        cipher = Fernet(key)
        return cipher.decrypt(encryption)
    
    def __str__(self):
       return f"ShareLink(user={self.user} content_path={self.content_path})"

        
class ShareLinkUsage(models.Model):

    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, related_name='user')
    owner = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, related_name='owner')
    share_link = models.ForeignKey(ShareLink, null=True, on_delete=models.SET_NULL)
    access_events = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PageView(models.Model):

    user = models.ForeignKey(AppUser, null=True, on_delete=models.SET_NULL)
    content_path = models.CharField(max_length=444)
    created_at = models.DateTimeField(auto_now_add=True)
    share_link = models.ForeignKey(ShareLink, on_delete=models.SET_NULL, null=True)


class Project(models.Model):

    name = models.CharField(max_length=444)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectGroupPermission(models.Model):

    department = models.ForeignKey(Project, on_delete=models.CASCADE)
    group = models.ManyToManyField(Group)
