from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from tasks.models import User, Task


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'phone', 'is_staff')
    search_fields = ('email', 'phone')
    ordering = ('email',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'execution_at', 'is_done')