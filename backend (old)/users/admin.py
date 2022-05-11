from django.contrib import admin
from .models import RipeUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Register your models here.


class RipeUserInline(admin.TabularInline):
    model = RipeUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [RipeUserInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
