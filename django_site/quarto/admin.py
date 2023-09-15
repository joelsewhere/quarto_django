from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AppUserCreationForm, UserChangeForm, ProjectGroupPermissionForm
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
    list_display = ('created_at', 'user', 'content_path', 'share_link')

@admin.register(models.ShareLink)
class ShareLinkAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'content_path', 'created_at', 'id')


@admin.register(models.ShareLinkUsage)
class ShareLinkUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'owner', 'share_link', 'access_events', 'created_at', 'updated_at')
    list_display_links = ["share_link"]


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(models.ProjectGroupPermission)
class ProjectGroupPermissionAdmin(admin.ModelAdmin):
    form = ProjectGroupPermissionForm
    add_form = ProjectGroupPermissionForm 
    list_display = ("department",)
    list_display_links = ["department"]
    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during foo creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)
