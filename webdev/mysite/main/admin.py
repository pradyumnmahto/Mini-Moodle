from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import NewUserForm
from .models import User, Course, Assignment,AssignmentSubmission

class CustomUserAdmin(UserAdmin):
    """ Creates a model for a custom user admin"""
    add_form = NewUserForm
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('username', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ['username']
    ordering = ['username']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)