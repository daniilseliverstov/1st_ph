from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Department, User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'department', 'is_staff')
    list_filter = ('department', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Работа', {'fields': ('department',)}),
    )


admin.site.register(Department)
admin.site.register(User, CustomUserAdmin)
