from django.contrib import admin
from .models import Routine, Task, TaskCompletion, RoutineSchedule


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'is_active', 'created_at', 'task_count']
    list_filter = ['is_active', 'created_at', 'created_by__role']
    search_fields = ['title', 'description', 'created_by__email']
    filter_horizontal = ['assigned_to']
    readonly_fields = ['created_at', 'updated_at']
    
    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'Tasks'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'routine', 'order', 'estimated_duration', 'is_required']
    list_filter = ['is_required', 'routine__is_active', 'created_at']
    search_fields = ['title', 'description', 'routine__title']
    ordering = ['routine', 'order']
    readonly_fields = ['created_at']


@admin.register(TaskCompletion)
class TaskCompletionAdmin(admin.ModelAdmin):
    list_display = ['task', 'child', 'completed_at', 'completed_by']
    list_filter = ['completed_at', 'task__routine__is_active']
    search_fields = ['task__title', 'child__email', 'notes']
    readonly_fields = ['completed_at']
    date_hierarchy = 'completed_at'


@admin.register(RoutineSchedule)
class RoutineScheduleAdmin(admin.ModelAdmin):
    list_display = ['routine', 'child', 'day_of_week', 'start_time', 'is_active']
    list_filter = ['day_of_week', 'is_active', 'routine__is_active']
    search_fields = ['routine__title', 'child__email']
    ordering = ['day_of_week', 'start_time']
