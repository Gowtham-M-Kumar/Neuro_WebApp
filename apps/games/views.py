from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction
import json
import random
from datetime import datetime

from .models import (
    Game, ColorMatchingGame, Color, ColorMatchingLevel,
    GameSession, ColorMatchingSession, GameProgress
)

@login_required
def games_dashboard(request):
    """Display available games"""
    games = Game.objects.filter(is_active=True)
    progress = GameProgress.objects.filter(child=request.user)
    progress_dict = {p.game_id: p for p in progress}
    
    context = {
        'games': games,
        'progress': progress_dict,
        'progress_list': list(progress),
    }
    return render(request, 'games/dashboard.html', context)

@login_required
def color_matching_levels(request):
    """Display color matching game levels"""
    game = get_object_or_404(Game, name__icontains='color matching')
    levels = ColorMatchingGame.objects.filter(is_active=True).order_by('level')
    
    # Get user's progress for this game
    progress, created = GameProgress.objects.get_or_create(
        child=request.user,
        game=game,
        defaults={'highest_level_completed': 0}
    )
    
    context = {
        'game': game,
        'levels': levels,
        'progress': progress,
    }
    return render(request, 'games/color_matching_levels.html', context)

@login_required
def color_matching_game(request, level):
    """Play color matching game for specific level"""
    game = get_object_or_404(Game, name__icontains='color matching')
    level_obj = get_object_or_404(ColorMatchingGame, level=level, is_active=True)
    level_config = get_object_or_404(ColorMatchingLevel, game=level_obj)
    
    # Get colors for this level
    colors = list(level_config.colors.all())
    
    if not colors:
        return JsonResponse({'error': 'No colors configured for this level'}, status=400)
    
    # Create game session
    session, created = GameSession.objects.get_or_create(
        child=request.user,
        game=game,
        level=level,
        defaults={'started_at': timezone.now()}
    )
    
    # Prepare game data
    grid_size = level_config.grid_size
    num_colors_needed = (grid_size * grid_size) // 2
    
    # Select colors for this game
    game_colors = random.sample(colors, min(num_colors_needed, len(colors)))
    
    # Create pairs of cards
    cards = []
    for color in game_colors:
        cards.extend([color] * 2)  # Each color appears twice
    
    # Shuffle cards
    random.shuffle(cards)
    
    # Arrange cards in grid
    grid = []
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            card_index = i * grid_size + j
            if card_index < len(cards):
                row.append({
                    'id': card_index,
                    'color': cards[card_index].hex_code,
                    'name': cards[card_index].name,
                    'row': i,
                    'col': j
                })
        grid.append(row)
    
    context = {
        'game': game,
        'level': level_obj,
        'session': session,
        'grid': grid,
        'grid_size': grid_size,
        'time_limit': level_obj.time_limit,
        'required_matches': level_obj.required_matches,
        'colors': game_colors,
    }
    return render(request, 'games/color_matching.html', context)

@csrf_exempt
@login_required
def save_game_result(request):
    """Save game session results via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            score = data.get('score', 0)
            time_taken = data.get('time_taken', 0)
            matches_found = data.get('matches_found', 0)
            total_attempts = data.get('total_attempts', 0)
            completed = data.get('completed', False)
            
            with transaction.atomic():
                # Update game session
                session = GameSession.objects.get(id=session_id, child=request.user)
                session.score = score
                session.time_taken = time_taken
                session.completed = completed
                if completed:
                    session.completed_at = timezone.now()
                session.save()
                
                # Create or update color matching session data
                color_session, created = ColorMatchingSession.objects.get_or_create(
                    game_session=session,
                    defaults={
                        'matches_found': matches_found,
                        'total_attempts': total_attempts,
                        'accuracy': (matches_found / total_attempts * 100) if total_attempts > 0 else 0
                    }
                )
                
                if not created:
                    color_session.matches_found = matches_found
                    color_session.total_attempts = total_attempts
                    color_session.accuracy = (matches_found / total_attempts * 100) if total_attempts > 0 else 0
                    color_session.save()
                
                # Update game progress
                progress, created = GameProgress.objects.get_or_create(
                    child=request.user,
                    game=session.game,
                    defaults={
                        'highest_level_completed': session.level if completed else 0,
                        'total_score': score,
                        'total_sessions': 1,
                        'average_accuracy': color_session.accuracy,
                        'last_played': timezone.now()
                    }
                )
                
                if not created:
                    progress.total_score += score
                    progress.total_sessions += 1
                    if completed and session.level > progress.highest_level_completed:
                        progress.highest_level_completed = session.level
                    
                    # Update average accuracy
                    all_sessions = ColorMatchingSession.objects.filter(
                        game_session__child=request.user,
                        game_session__game=session.game
                    )
                    total_accuracy = sum(s.accuracy for s in all_sessions)
                    progress.average_accuracy = total_accuracy / all_sessions.count()
                    
                    progress.last_played = timezone.now()
                    progress.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Game result saved successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def game_progress(request):
    """Display user's game progress"""
    progress_list = GameProgress.objects.filter(child=request.user).order_by('-updated_at')
    
    context = {
        'progress_list': progress_list,
    }
    return render(request, 'games/progress.html', context)

@login_required
def game_history(request):
    """Display user's game session history"""
    sessions = GameSession.objects.filter(child=request.user).order_by('-started_at')
    
    context = {
        'sessions': sessions,
    }
    return render(request, 'games/history.html', context)
