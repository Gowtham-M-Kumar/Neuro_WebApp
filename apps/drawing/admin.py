from django.contrib import admin
from .models import Drawing, DrawingSession


@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    list_display = ['title', 'child', 'created_at', 'updated_at', 'is_completed', 'version_number']
    list_filter = ['is_completed', 'created_at', 'updated_at', 'child__role']
    search_fields = ['title', 'child__first_name', 'child__last_name', 'child__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'child', 'is_completed')
        }),
        ('Canvas Data', {
            'fields': ('canvas_data', 'canvas_width', 'canvas_height'),
            'classes': ('collapse',)
        }),
        ('Sharing Settings', {
            'fields': ('shared_with_parents', 'shared_with_therapists', 'shared_with_teachers')
        }),
        ('Version Control', {
            'fields': ('parent_drawing', 'version_number'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('child')


@admin.register(DrawingSession)
class DrawingSessionAdmin(admin.ModelAdmin):
    list_display = ['drawing', 'child', 'started_at', 'ended_at', 'duration_seconds', 'strokes_count']
    list_filter = ['started_at', 'ended_at', 'child__role']
    search_fields = ['drawing__title', 'child__first_name', 'child__last_name']
    readonly_fields = ['started_at', 'ended_at']
    
    fieldsets = (
        ('Session Information', {
            'fields': ('drawing', 'child', 'duration_seconds')
        }),
        ('Timestamps', {
            'fields': ('started_at', 'ended_at')
        }),
        ('Analytics', {
            'fields': ('strokes_count', 'colors_used', 'tools_used'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('drawing', 'child')
