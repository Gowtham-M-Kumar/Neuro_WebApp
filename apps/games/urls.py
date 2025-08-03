from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.games_dashboard, name='dashboard'),
    path('color-matching/', views.color_matching_levels, name='color_matching_levels'),
    path('color-matching/level/<int:level>/', views.color_matching_game, name='color_matching_game'),
    path('progress/', views.game_progress, name='progress'),
    path('history/', views.game_history, name='history'),
    path('api/save-result/', views.save_game_result, name='save_result'),
] 