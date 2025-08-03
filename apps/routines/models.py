from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Routine(models.Model):
    """Visual schedule/routine for children"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_routines'
    )
    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='assigned_routines',
        limit_choices_to={'role': 'child'}
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Task(models.Model):
    """Individual task within a routine"""
    routine = models.ForeignKey(
        Routine,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='task_images/',
        blank=True,
        null=True,
        help_text=_('Visual representation of the task')
    )
    order = models.PositiveIntegerField(default=0)
    estimated_duration = models.PositiveIntegerField(
        default=5,
        help_text=_('Estimated duration in minutes')
    )
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['routine', 'order']
    
    def __str__(self):
        return f"{self.routine.title} - {self.title}"


class TaskCompletion(models.Model):
    """Track completion of tasks by children"""
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='completions'
    )
    child = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='task_completions',
        limit_choices_to={'role': 'child'}
    )
    completed_at = models.DateTimeField(auto_now_add=True)
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marked_completions'
    )
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['task', 'child', 'completed_at']
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.child.get_full_name()} completed {self.task.title}"


class RoutineSchedule(models.Model):
    """Schedule when routines should be performed"""
    routine = models.ForeignKey(
        Routine,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    child = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='routine_schedules',
        limit_choices_to={'role': 'child'}
    )
    day_of_week = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday'),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['routine', 'child', 'day_of_week']
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.routine.title} - {self.child.get_full_name()} - {self.get_day_of_week_display()}"
