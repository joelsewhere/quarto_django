from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from . import models


class AppUserCreationForm(UserCreationForm):

    class Meta:
        model = models.AppUser
        fields = ("email",)


class UserChangeForm(UserChangeForm):

    class Meta:
        model = models.AppUser
        fields = ("email",)

