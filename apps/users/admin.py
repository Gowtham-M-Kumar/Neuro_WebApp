from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, ParentProfile, TherapistProfile, TeacherProfile, ChildProfile


class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser"""
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'profile_picture')}),
        (_('Role'), {'fields': ('role',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'first_name', 'last_name'),
        }),
    )


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'emergency_contact', 'children_count')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    filter_horizontal = ('children',)
    
    def children_count(self, obj):
        return obj.children.count()
    children_count.short_description = 'Number of Children'


@admin.register(TherapistProfile)
class TherapistProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'years_of_experience', 'assigned_children_count')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'license_number')
    filter_horizontal = ('assigned_children',)
    
    def assigned_children_count(self, obj):
        return obj.assigned_children.count()
    assigned_children_count.short_description = 'Assigned Children'


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'classroom_info', 'grade_level', 'assigned_children_count')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'classroom_info')
    filter_horizontal = ('assigned_children',)
    
    def assigned_children_count(self, obj):
        return obj.assigned_children.count()
    assigned_children_count.short_description = 'Assigned Children'


@admin.register(ChildProfile)
class ChildProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'learning_level', 'primary_parent', 'primary_therapist')
    list_filter = ('learning_level', 'age')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    autocomplete_fields = ('primary_parent', 'primary_therapist', 'primary_teacher')


# Register the custom user admin
admin.site.register(CustomUser, CustomUserAdmin)
