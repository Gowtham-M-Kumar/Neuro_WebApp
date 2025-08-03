from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Routine, Task, TaskCompletion, RoutineSchedule
from .forms import (
    RoutineForm, TaskForm, TaskCompletionForm, 
    RoutineScheduleForm, TaskReorderForm
)


@login_required
def routine_list(request):
    """Display list of routines based on user role"""
    user = request.user
    
    if user.role == 'child':
        # Children see their assigned routines
        routines = Routine.objects.filter(
            assigned_to=user,
            is_active=True
        )
    elif user.role == 'parent':
        # Parents see routines assigned to their children
        children = user.parent_profile.children.all()
        child_users = [child.user for child in children]
        routines = Routine.objects.filter(
            assigned_to__in=child_users,
            is_active=True
        ).distinct()
    elif user.role in ['therapist', 'teacher']:
        # Therapists/Teachers see routines they created
        routines = Routine.objects.filter(created_by=user)
    else:
        routines = Routine.objects.none()
    
    context = {
        'routines': routines,
        'user_role': user.role
    }
    return render(request, 'routines/routine_list.html', context)


@login_required
def routine_detail(request, routine_id):
    """Display routine details and tasks"""
    routine = get_object_or_404(Routine, id=routine_id)
    user = request.user
    
    # Check permissions
    if user.role == 'child' and user not in routine.assigned_to.all():
        messages.error(request, "You don't have permission to view this routine.")
        return redirect('routines:routine_list')
    elif user.role == 'parent':
        children = user.parent_profile.children.all()
        child_user_ids = [child.user.id for child in children]
        if not routine.assigned_to.filter(id__in=child_user_ids).exists():
            messages.error(request, "You don't have permission to view this routine.")
            return redirect('routines:routine_list')
    elif user.role in ['therapist', 'teacher'] and routine.created_by != user:
        messages.error(request, "You don't have permission to view this routine.")
        return redirect('routines:routine_list')
    
    tasks = routine.tasks.all()
    
    # Get completion status for children
    if user.role == 'child':
        task_completions = TaskCompletion.objects.filter(
            task__routine=routine,
            child=user
        ).values_list('task_id', flat=True)
    elif user.role == 'parent':
        children = user.parent_profile.children.all()
        child_users = [child.user for child in children]
        task_completions = TaskCompletion.objects.filter(
            task__routine=routine,
            child__in=child_users
        ).values_list('task_id', 'child_id')
    else:
        task_completions = []
    
    context = {
        'routine': routine,
        'tasks': tasks,
        'task_completions': task_completions,
        'user_role': user.role
    }
    return render(request, 'routines/routine_detail.html', context)


@login_required
def routine_create(request):
    """Create a new routine"""
    if request.user.role not in ['therapist', 'teacher']:
        messages.error(request, "Only therapists and teachers can create routines.")
        return redirect('routines:routine_list')
    
    if request.method == 'POST':
        form = RoutineForm(request.POST, user=request.user)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.created_by = request.user
            routine.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, f"Routine '{routine.title}' created successfully!")
            return redirect('routines:routine_detail', routine_id=routine.id)
    else:
        form = RoutineForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Create New Routine'
    }
    return render(request, 'routines/routine_form.html', context)


@login_required
def routine_edit(request, routine_id):
    """Edit an existing routine"""
    routine = get_object_or_404(Routine, id=routine_id)
    
    if request.user.role not in ['therapist', 'teacher'] or routine.created_by != request.user:
        messages.error(request, "You don't have permission to edit this routine.")
        return redirect('routines:routine_detail', routine_id=routine.id)
    
    if request.method == 'POST':
        form = RoutineForm(request.POST, instance=routine, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Routine '{routine.title}' updated successfully!")
            return redirect('routines:routine_detail', routine_id=routine.id)
    else:
        form = RoutineForm(instance=routine, user=request.user)
    
    context = {
        'form': form,
        'routine': routine,
        'title': f'Edit Routine: {routine.title}'
    }
    return render(request, 'routines/routine_form.html', context)


@login_required
def task_create(request, routine_id):
    """Add a new task to a routine"""
    routine = get_object_or_404(Routine, id=routine_id)
    
    if request.user.role not in ['therapist', 'teacher'] or routine.created_by != request.user:
        messages.error(request, "You don't have permission to add tasks to this routine.")
        return redirect('routines:routine_detail', routine_id=routine.id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.routine = routine
            task.save()
            messages.success(request, f"Task '{task.title}' added successfully!")
            return redirect('routines:routine_detail', routine_id=routine.id)
    else:
        form = TaskForm()
    
    context = {
        'form': form,
        'routine': routine,
        'title': f'Add Task to {routine.title}'
    }
    return render(request, 'routines/task_form.html', context)


@login_required
def task_edit(request, task_id):
    """Edit an existing task"""
    task = get_object_or_404(Task, id=task_id)
    
    if request.user.role not in ['therapist', 'teacher'] or task.routine.created_by != request.user:
        messages.error(request, "You don't have permission to edit this task.")
        return redirect('routines:routine_detail', routine_id=task.routine.id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f"Task '{task.title}' updated successfully!")
            return redirect('routines:routine_detail', routine_id=task.routine.id)
    else:
        form = TaskForm(instance=task)
    
    context = {
        'form': form,
        'task': task,
        'routine': task.routine,
        'title': f'Edit Task: {task.title}'
    }
    return render(request, 'routines/task_form.html', context)


@login_required
@require_POST
def task_complete(request, task_id):
    """Mark a task as completed"""
    task = get_object_or_404(Task, id=task_id)
    user = request.user
    
    # Check if user can complete this task
    if user.role == 'child':
        if user not in task.routine.assigned_to.all():
            messages.error(request, "You don't have permission to complete this task.")
            return redirect('routines:routine_detail', routine_id=task.routine.id)
    elif user.role == 'parent':
        children = user.parent_profile.children.all()
        child_user_ids = [child.user.id for child in children]
        if not task.routine.assigned_to.filter(id__in=child_user_ids).exists():
            messages.error(request, "You don't have permission to complete this task.")
            return redirect('routines:routine_detail', routine_id=task.routine.id)
    else:
        messages.error(request, "Only children and parents can complete tasks.")
        return redirect('routines:routine_detail', routine_id=task.routine.id)
    
    # Determine which child completed the task
    if user.role == 'child':
        child = user
    else:
        # Parent completing for a child - need to specify which child
        child_id = request.POST.get('child_id')
        if not child_id:
            messages.error(request, "Please specify which child completed the task.")
            return redirect('routines:routine_detail', routine_id=task.routine.id)
        child_profile = get_object_or_404(user.parent_profile.children.all(), id=child_id)
        child = child_profile.user
    
    # Check if already completed today
    today = timezone.now().date()
    existing_completion = TaskCompletion.objects.filter(
        task=task,
        child=child,
        completed_at__date=today
    ).first()
    
    if existing_completion:
        messages.warning(request, "This task was already completed today.")
        return redirect('routines:routine_detail', routine_id=task.routine.id)
    
    # Create completion record
    completion = TaskCompletion.objects.create(
        task=task,
        child=child,
        completed_by=user
    )
    
    messages.success(request, f"Task '{task.title}' marked as completed!")
    return redirect('routines:routine_detail', routine_id=task.routine.id)


@login_required
@csrf_exempt
@require_POST
def task_reorder(request):
    """Reorder tasks via AJAX"""
    if request.user.role not in ['therapist', 'teacher']:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    form = TaskReorderForm(request.POST)
    if form.is_valid():
        task = form.cleaned_data['task']
        new_order = form.cleaned_data['new_order']
        
        if task.routine.created_by != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        # Update task order
        task.order = new_order
        task.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid data'}, status=400)


@login_required
def routine_schedule(request, routine_id):
    """Schedule a routine for specific times"""
    routine = get_object_or_404(Routine, id=routine_id)
    
    if request.user.role not in ['therapist', 'teacher'] or routine.created_by != request.user:
        messages.error(request, "You don't have permission to schedule this routine.")
        return redirect('routines:routine_detail', routine_id=routine.id)
    
    if request.method == 'POST':
        form = RoutineScheduleForm(request.POST, user=request.user)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.routine = routine
            schedule.save()
            messages.success(request, "Routine scheduled successfully!")
            return redirect('routines:routine_detail', routine_id=routine.id)
    else:
        form = RoutineScheduleForm(user=request.user)
    
    # Get existing schedules
    schedules = RoutineSchedule.objects.filter(routine=routine)
    
    context = {
        'form': form,
        'routine': routine,
        'schedules': schedules,
        'title': f'Schedule Routine: {routine.title}'
    }
    return render(request, 'routines/routine_schedule.html', context)


@login_required
def routine_progress(request, routine_id):
    """View progress for a routine"""
    routine = get_object_or_404(Routine, id=routine_id)
    user = request.user
    
    # Check permissions
    if user.role == 'child' and user not in routine.assigned_to.all():
        messages.error(request, "You don't have permission to view this routine.")
        return redirect('routines:routine_list')
    elif user.role == 'parent':
        children = user.parent_profile.children.all()
        child_user_ids = [child.user.id for child in children]
        if not routine.assigned_to.filter(id__in=child_user_ids).exists():
            messages.error(request, "You don't have permission to view this routine.")
            return redirect('routines:routine_list')
    elif user.role in ['therapist', 'teacher'] and routine.created_by != user:
        messages.error(request, "You don't have permission to view this routine.")
        return redirect('routines:routine_list')
    
    # Get completion data
    if user.role == 'child':
        children = [user]
    elif user.role == 'parent':
        children_profiles = user.parent_profile.children.all()
        children = [child_profile.user for child_profile in children_profiles]
    else:
        children = routine.assigned_to.all()
    
    # Get completion statistics
    completion_stats = []
    for child in children:
        if child in routine.assigned_to.all():
            total_tasks = routine.tasks.count()
            completed_tasks = TaskCompletion.objects.filter(
                task__routine=routine,
                child=child
            ).count()
            
            completion_stats.append({
                'child': child,
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
            })
    
    context = {
        'routine': routine,
        'completion_stats': completion_stats,
        'user_role': user.role
    }
    return render(request, 'routines/routine_progress.html', context)
