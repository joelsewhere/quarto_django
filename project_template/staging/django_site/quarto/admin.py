from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import (
    AppUserCreationForm,
    UserChangeForm,
    
    )
from . import models


@admin.register(models.AppUser)
class AppUserAdmin(UserAdmin):
    add_form = AppUserCreationForm
    form = UserChangeForm
    model = models.AppUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(models.PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('created_at',
                    'user',
                    'content_path',
                    
                    )



