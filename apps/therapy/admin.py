from django.contrib import admin
from .models import (
    TherapyActivity, ActivityItem, ActivityAssignment, 
    ActivityAttempt, ActivityProgress
)


@admin.register(TherapyActivity)
class TherapyActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity_type', 'difficulty_level', 'created_by', 'is_active', 'item_count']
    list_filter = ['activity_type', 'difficulty_level', 'is_active', 'created_at', 'created_by__role']
    search_fields = ['title', 'description', 'instructions', 'created_by__email']
    readonly_fields = ['created_at', 'updated_at']
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


@admin.register(ActivityItem)
class ActivityItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity', 'order', 'is_correct_answer', 'group_id']
    list_filter = ['is_correct_answer', 'activity__activity_type', 'activity__is_active']
    search_fields = ['title', 'activity__title', 'group_id']
    ordering = ['activity', 'order']


@admin.register(ActivityAssignment)
class ActivityAssignmentAdmin(admin.ModelAdmin):
    list_display = ['activity', 'child', 'assigned_by', 'assigned_at', 'is_completed', 'due_date']
    list_filter = ['is_completed', 'assigned_at', 'due_date', 'activity__activity_type']
    search_fields = ['activity__title', 'child__email', 'assigned_by__email', 'notes']
    readonly_fields = ['assigned_at']
    date_hierarchy = 'assigned_at'


@admin.register(ActivityAttempt)
class ActivityAttemptAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'started_at', 'completed_at', 'score', 'max_score', 'is_successful', 'time_taken']
    list_filter = ['is_successful', 'started_at', 'assignment__activity__activity_type']
    search_fields = ['assignment__child__email', 'assignment__activity__title', 'notes']
    readonly_fields = ['started_at', 'completed_at', 'percentage_score']
    date_hierarchy = 'started_at'


@admin.register(ActivityProgress)
class ActivityProgressAdmin(admin.ModelAdmin):
    list_display = ['child', 'activity_type', 'total_attempts', 'successful_attempts', 'success_rate', 'average_score', 'best_score']
    list_filter = ['activity_type', 'created_at', 'updated_at']
    search_fields = ['child__email', 'child__first_name', 'child__last_name']
    readonly_fields = ['created_at', 'updated_at', 'success_rate']
    ordering = ['-updated_at']
