from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Avg, Count, Sum, Max
from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    TherapyActivity, ActivityItem, ActivityAssignment, 
    ActivityAttempt, ActivityProgress
)
from .forms import (
    TherapyActivityForm, ActivityItemForm, ActivityAssignmentForm,
    ActivityAttemptForm, ActivityFilterForm, ProgressFilterForm
)
from apps.games.models import Game, GameProgress


@login_required
def activity_list(request):
    """Display list of therapy activities based on user role"""
    user = request.user
    
    if user.role == 'child':
        # Children see their assigned activities
        activities = TherapyActivity.objects.filter(
            assignments__child=user,
            assignments__is_completed=False
        ).distinct()
    elif user.role == 'parent':
        # Parents see activities assigned to their children
        children = user.parent_profile.children.all()
        child_users = [child.user for child in children]
        activities = TherapyActivity.objects.filter(
            assignments__child__in=child_users
        ).distinct()
    elif user.role in ['therapist', 'teacher']:
        # Therapists/Teachers see activities they created
        activities = TherapyActivity.objects.filter(created_by=user)
    else:
        activities = TherapyActivity.objects.none()
    
    # Apply filters
    filter_form = ActivityFilterForm(request.GET)
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('activity_type'):
            activities = activities.filter(
                activity_type=filter_form.cleaned_data['activity_type']
            )
        if filter_form.cleaned_data.get('difficulty_level'):
            activities = activities.filter(
                difficulty_level=filter_form.cleaned_data['difficulty_level']
            )
        if filter_form.cleaned_data.get('is_active'):
            is_active_value = filter_form.cleaned_data['is_active']
            if is_active_value in ['True', 'False']:
                activities = activities.filter(
                    is_active=(is_active_value == 'True')
                )
        if filter_form.cleaned_data.get('search'):
            search_term = filter_form.cleaned_data['search']
            activities = activities.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            )
    
    context = {
        'activities': activities,
        'filter_form': filter_form,
        'user_role': user.role
    }
    return render(request, 'therapy/activity_list.html', context)


@login_required
def activity_detail(request, activity_id):
    """Display activity details and items"""
    activity = get_object_or_404(TherapyActivity, id=activity_id)
    user = request.user
    
    # Check permissions and get assignment
    assignment = None
    if user.role == 'child':
        assignment = ActivityAssignment.objects.filter(
            activity=activity,
            child=user
        ).first()
        if not assignment:
            messages.error(request, "You don't have permission to view this activity.")
            return redirect('therapy:activity_list')
    elif user.role == 'parent':
        children = user.parent_profile.children.all()
        child_users = [child.user for child in children]
        assignment = ActivityAssignment.objects.filter(
            activity=activity,
            child__in=child_users
        ).first()
        if not assignment:
            messages.error(request, "You don't have permission to view this activity.")
            return redirect('therapy:activity_list')
    elif user.role in ['therapist', 'teacher'] and activity.created_by != user:
        messages.error(request, "You don't have permission to view this activity.")
        return redirect('therapy:activity_list')
    
    items = activity.items.all()
    
    # Get assignment info for children
    if user.role == 'child':
        assignments = [ActivityAssignment.objects.filter(
            activity=activity,
            child=user
        ).first()]
    elif user.role == 'parent':
        children = user.parent_profile.children.all()
        child_users = [child.user for child in children]
        assignments = ActivityAssignment.objects.filter(
            activity=activity,
            child__in=child_users
        )
    else:
        assignments = ActivityAssignment.objects.filter(activity=activity)
    
    context = {
        'activity': activity,
        'items': items,
        'assignments': assignments,
        'assignment': assignment,
        'user_role': user.role,
        'user': user
    }
    return render(request, 'therapy/activity_detail.html', context)


@login_required
def activity_create(request):
    """Create a new therapy activity"""
    if request.user.role not in ['therapist', 'teacher']:
        messages.error(request, "Only therapists and teachers can create activities.")
        return redirect('therapy:activity_list')
    
    if request.method == 'POST':
        form = TherapyActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.created_by = request.user
            activity.save()
            messages.success(request, f"Activity '{activity.title}' created successfully!")
            return redirect('therapy:activity_detail', activity_id=activity.id)
    else:
        form = TherapyActivityForm()
    
    context = {
        'form': form,
        'title': 'Create New Activity'
    }
    return render(request, 'therapy/activity_form.html', context)


@login_required
def activity_edit(request, activity_id):
    """Edit an existing therapy activity"""
    activity = get_object_or_404(TherapyActivity, id=activity_id)
    
    if request.user.role not in ['therapist', 'teacher'] or activity.created_by != request.user:
        messages.error(request, "You don't have permission to edit this activity.")
        return redirect('therapy:activity_detail', activity_id=activity.id)
    
    if request.method == 'POST':
        form = TherapyActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, f"Activity '{activity.title}' updated successfully!")
            return redirect('therapy:activity_detail', activity_id=activity.id)
    else:
        form = TherapyActivityForm(instance=activity)
    
    context = {
        'form': form,
        'activity': activity,
        'title': f'Edit Activity: {activity.title}'
    }
    return render(request, 'therapy/activity_form.html', context)


@login_required
def item_create(request, activity_id):
    """Add a new item to an activity"""
    activity = get_object_or_404(TherapyActivity, id=activity_id)
    
    if request.user.role not in ['therapist', 'teacher'] or activity.created_by != request.user:
        messages.error(request, "You don't have permission to add items to this activity.")
        return redirect('therapy:activity_detail', activity_id=activity.id)
    
    if request.method == 'POST':
        form = ActivityItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.activity = activity
            item.save()
            messages.success(request, f"Item '{item.title}' added successfully!")
            return redirect('therapy:activity_detail', activity_id=activity.id)
    else:
        form = ActivityItemForm()
    
    context = {
        'form': form,
        'activity': activity,
        'title': f'Add Item to {activity.title}'
    }
    return render(request, 'therapy/item_form.html', context)


@login_required
def item_edit(request, item_id):
    """Edit an existing activity item"""
    item = get_object_or_404(ActivityItem, id=item_id)
    
    if request.user.role not in ['therapist', 'teacher'] or item.activity.created_by != request.user:
        messages.error(request, "You don't have permission to edit this item.")
        return redirect('therapy:activity_detail', activity_id=item.activity.id)
    
    if request.method == 'POST':
        form = ActivityItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Item '{item.title}' updated successfully!")
            return redirect('therapy:activity_detail', activity_id=item.activity.id)
    else:
        form = ActivityItemForm(instance=item)
    
    context = {
        'form': form,
        'item': item,
        'activity': item.activity,
        'title': f'Edit Item: {item.title}'
    }
    return render(request, 'therapy/item_form.html', context)


@login_required
def activity_assign(request, activity_id):
    """Assign an activity to children"""
    activity = get_object_or_404(TherapyActivity, id=activity_id)
    
    if request.user.role not in ['therapist', 'teacher'] or activity.created_by != request.user:
        messages.error(request, "You don't have permission to assign this activity.")
        return redirect('therapy:activity_detail', activity_id=activity.id)
    
    if request.method == 'POST':
        form = ActivityAssignmentForm(request.POST, user=request.user)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.activity = activity
            assignment.assigned_by = request.user
            assignment.save()
            messages.success(request, f"Activity assigned to {assignment.child.get_full_name()} successfully!")
            return redirect('therapy:activity_detail', activity_id=activity.id)
    else:
        form = ActivityAssignmentForm(user=request.user)
    
    # Get existing assignments
    assignments = ActivityAssignment.objects.filter(activity=activity)
    
    context = {
        'form': form,
        'activity': activity,
        'assignments': assignments,
        'title': f'Assign Activity: {activity.title}'
    }
    return render(request, 'therapy/activity_assign.html', context)


@login_required
def activity_play(request, assignment_id):
    """Play/attempt an activity"""
    assignment = get_object_or_404(ActivityAssignment, id=assignment_id)
    user = request.user
    
    # Check permissions
    if user.role == 'child' and assignment.child != user:
        messages.error(request, "You don't have permission to play this activity.")
        return redirect('therapy:activity_list')
    elif user.role == 'parent':
        children = user.parent_profile.children.all()
        child_users = [child.user for child in children]
        if assignment.child not in child_users:
            messages.error(request, "You don't have permission to play this activity.")
            return redirect('therapy:activity_list')
    else:
        messages.error(request, "Only children and parents can play activities.")
        return redirect('therapy:activity_list')
    
    activity = assignment.activity
    items = activity.items.all()
    
    # Get previous attempts
    attempts = ActivityAttempt.objects.filter(assignment=assignment).order_by('-started_at')
    
    context = {
        'assignment': assignment,
        'activity': activity,
        'items': items,
        'attempts': attempts,
        'user_role': user.role
    }
    return render(request, 'therapy/activity_play.html', context)


@login_required
@require_POST
def activity_submit(request, assignment_id):
    """Submit activity attempt results"""
    assignment = get_object_or_404(ActivityAssignment, id=assignment_id)
    user = request.user
    
    # Check permissions
    if user.role == 'child' and assignment.child != user:
        messages.error(request, "You don't have permission to submit this activity.")
        return redirect('therapy:activity_list')
    elif user.role == 'parent':
        children = user.parent_profile.children.all()
        child_users = [child.user for child in children]
        if assignment.child not in child_users:
            messages.error(request, "You don't have permission to submit this activity.")
            return redirect('therapy:activity_list')
    else:
        messages.error(request, "Only children and parents can submit activities.")
        return redirect('therapy:activity_list')
    
    # Get form data
    form = ActivityAttemptForm(request.POST)
    if form.is_valid():
        attempt = form.save(commit=False)
        attempt.assignment = assignment
        attempt.completed_at = timezone.now()
        
        # Calculate time taken if not provided
        if not attempt.time_taken:
            # This would need to be calculated from frontend
            attempt.time_taken = 0
        
        attempt.save()
        
        # Update progress
        progress, created = ActivityProgress.objects.get_or_create(
            child=assignment.child,
            activity_type=assignment.activity.activity_type,
            defaults={
                'total_attempts': 0,
                'successful_attempts': 0,
                'average_score': 0,
                'best_score': 0
            }
        )
        
        progress.total_attempts += 1
        if attempt.is_successful:
            progress.successful_attempts += 1
        
        # Update average score
        all_attempts = ActivityAttempt.objects.filter(assignment__child=assignment.child)
        if all_attempts.exists():
            progress.average_score = all_attempts.aggregate(Avg('score'))['score__avg'] or 0
        
        # Update best score
        if attempt.score and attempt.score > progress.best_score:
            progress.best_score = attempt.score
        
        progress.last_attempt_date = timezone.now()
        progress.save()
        
        messages.success(request, f"Activity completed! Score: {attempt.score}/{attempt.max_score}")
        return redirect('therapy:activity_detail', activity_id=assignment.activity.id)
    
    messages.error(request, "Invalid submission data.")
    return redirect('therapy:activity_play', assignment_id=assignment_id)


@login_required
def game_dashboard(request):
    """Game dashboard for children - Color Matching Game only"""
    user = request.user
    
    if user.role != 'child':
        messages.error(request, "This dashboard is only for children.")
        return redirect('therapy:activity_list')
    
    # Get Color Matching Game from games app
    color_matching_game = Game.objects.filter(name="Color Matching Game", is_active=True).first()
    color_matching_progress = None
    color_matching_progress_value = 0
    if color_matching_game:
        color_matching_progress = GameProgress.objects.filter(
            game=color_matching_game,
            child=user
        ).first()
        if color_matching_progress:
            # Calculate progress: 157 - (level * 31.4) where 157 is full circle, 31.4 is per level
            color_matching_progress_value = 157 - (color_matching_progress.highest_level_completed * 31.4)
        else:
            color_matching_progress_value = 157  # No progress, full circle
    
    # Calculate statistics for Color Matching Game only
    total_activities = 1 if color_matching_game else 0
    completed_activities = 1 if color_matching_progress and color_matching_progress.highest_level_completed >= 5 else 0
    average_score = color_matching_progress.total_score if color_matching_progress else 0
    total_time = color_matching_progress.total_sessions * 2 if color_matching_progress else 0  # Estimate 2 minutes per session
    
    context = {
        'color_matching_game': color_matching_game,
        'color_matching_progress': color_matching_progress,
        'color_matching_progress_value': color_matching_progress_value,
        'total_activities': total_activities,
        'completed_activities': completed_activities,
        'average_score': average_score,
        'total_time': total_time,  # Already in minutes
        'user_role': user.role
    }
    return render(request, 'therapy/game_dashboard.html', context)


@login_required
def progress_report(request):
    """View progress reports for activities"""
    user = request.user
    
    if user.role == 'child':
        children = [user]
    elif user.role == 'parent':
        children_profiles = user.parent_profile.children.all()
        children = [child_profile.user for child_profile in children_profiles]
    elif user.role in ['therapist', 'teacher']:
        # Get children assigned to this therapist/teacher
        if user.role == 'therapist':
            children_profiles = user.therapist_profile.assigned_children.all()
            children = [child_profile.user for child_profile in children_profiles]
        else:
            children_profiles = user.teacher_profile.assigned_children.all()
            children = [child_profile.user for child_profile in children_profiles]
    else:
        children = []
    
    # Apply filters
    filter_form = ProgressFilterForm(request.GET)
    if filter_form.is_valid():
        activity_type = filter_form.cleaned_data.get('activity_type')
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        
        progress_queryset = ActivityProgress.objects.filter(child__in=children)
        
        if activity_type:
            progress_queryset = progress_queryset.filter(activity_type=activity_type)
        if date_from:
            progress_queryset = progress_queryset.filter(last_attempt_date__date__gte=date_from)
        if date_to:
            progress_queryset = progress_queryset.filter(last_attempt_date__date__lte=date_to)
    else:
        progress_queryset = ActivityProgress.objects.filter(child__in=children)
    
    progress_data = progress_queryset.order_by('-updated_at')
    
    context = {
        'progress_data': progress_data,
        'filter_form': filter_form,
        'children': children,
        'user_role': user.role
    }
    return render(request, 'therapy/progress_report.html', context)
