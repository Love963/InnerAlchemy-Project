from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin 
from .models import User
# Register your models here.
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_active', )
    search_fields = ('email', 'username')
    ordering = ('email', )
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'bio', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),

        }),
    )