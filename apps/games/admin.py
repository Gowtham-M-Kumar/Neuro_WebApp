from django.contrib import admin
from .models import (
    Game, ColorMatchingGame, Color, ColorMatchingLevel, 
    GameSession, ColorMatchingSession, GameProgress
)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']

@admin.register(ColorMatchingGame)
class ColorMatchingGameAdmin(admin.ModelAdmin):
    list_display = ['level', 'name', 'time_limit', 'required_matches', 'is_active']
    list_filter = ['is_active', 'level']
    search_fields = ['name', 'description']
    ordering = ['level']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'hex_code', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name']
    ordering = ['name']

@admin.register(ColorMatchingLevel)
class ColorMatchingLevelAdmin(admin.ModelAdmin):
    list_display = ['game', 'grid_size', 'shuffle_count', 'colors_count']
    list_filter = ['grid_size']
    filter_horizontal = ['colors']
    
    def colors_count(self, obj):
        return obj.colors.count()
    colors_count.short_description = 'Number of Colors'

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['child', 'game', 'level', 'score', 'time_taken', 'completed', 'started_at']
    list_filter = ['completed', 'game', 'level', 'started_at']
    search_fields = ['child__username', 'child__email']
    readonly_fields = ['started_at']

@admin.register(ColorMatchingSession)
class ColorMatchingSessionAdmin(admin.ModelAdmin):
    list_display = ['game_session', 'matches_found', 'total_attempts', 'accuracy']
    list_filter = ['matches_found', 'accuracy']
    readonly_fields = ['game_session']

@admin.register(GameProgress)
class GameProgressAdmin(admin.ModelAdmin):
    list_display = ['child', 'game', 'highest_level_completed', 'total_score', 'total_sessions', 'average_accuracy', 'last_played']
    list_filter = ['game', 'highest_level_completed', 'last_played']
    search_fields = ['child__username', 'child__email']
    readonly_fields = ['updated_at']
