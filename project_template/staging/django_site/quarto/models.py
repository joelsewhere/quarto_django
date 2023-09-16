import os
from cryptography.fernet import Fernet
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import AppUserManager


class AppUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(max_length=444)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AppUserManager()

    def __str__(self):
        return self.email



class PageView(models.Model):

    user = models.ForeignKey(AppUser, null=True, on_delete=models.SET_NULL)
    content_path = models.CharField(max_length=444)
    created_at = models.DateTimeField(auto_now_add=True)
    

