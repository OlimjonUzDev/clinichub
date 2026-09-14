from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


class UserAdmin(DjangoUserAdmin):
    model = User
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Qoshimcha (ClinicHub)",
            {'fields': ('role', 'phone_number', 'avatar')},
        ),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (
            "Qoshimcha (ClinicHub)",
            {'fields': ('role', 'phone_number', 'avatar')},
        ),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = DjangoUserAdmin.list_filter + ('role',)


admin.site.register(User, UserAdmin)