from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class TherapyActivity(models.Model):
    """Base therapy activity model"""
    
    class ActivityType(models.TextChoices):
        MATCHING = 'matching', _('Matching Game')
        FOCUS = 'focus', _('Focus Activity')
        MEMORY = 'memory', _('Memory Game')
        MOTOR = 'motor', _('Motor Skills')
        SORTING = 'sorting', _('Sorting Activity')
        SEQUENCING = 'sequencing', _('Sequencing Activity')
    
    class DifficultyLevel(models.TextChoices):
        EASY = 'easy', _('Easy')
        MEDIUM = 'medium', _('Medium')
        HARD = 'hard', _('Hard')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
        default=ActivityType.MATCHING
    )
    difficulty_level = models.CharField(
        max_length=10,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.EASY
    )
    instructions = models.TextField(help_text=_('Instructions for the child'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_activities',
        limit_choices_to={'role__in': ['therapist', 'teacher']}
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Therapy activities'
    
    def __str__(self):
        return f"{self.title} ({self.get_activity_type_display()})"


class ActivityItem(models.Model):
    """Individual items within an activity (e.g., cards for matching)"""
    activity = models.ForeignKey(
        TherapyActivity,
        on_delete=models.CASCADE,
        related_name='items'
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='activity_images/',
        blank=True,
        null=True
    )
    audio_file = models.FileField(
        upload_to='activity_audio/',
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(default=0)
    is_correct_answer = models.BooleanField(default=False)
    group_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=_('For grouping related items together')
    )
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.activity.title} - {self.title}"


class ActivityAssignment(models.Model):
    """Assign activities to specific children"""
    activity = models.ForeignKey(
        TherapyActivity,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    child = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_activities',
        limit_choices_to={'role': 'child'}
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_assignments',
        limit_choices_to={'role__in': ['therapist', 'teacher']}
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['activity', 'child']
        ordering = ['-assigned_at']
    
    def __str__(self):
        return f"{self.child.get_full_name()} - {self.activity.title}"


class ActivityAttempt(models.Model):
    """Track child's attempts at activities"""
    assignment = models.ForeignKey(
        ActivityAssignment,
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    score = models.PositiveIntegerField(blank=True, null=True)
    max_score = models.PositiveIntegerField(blank=True, null=True)
    time_taken = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_('Time taken in seconds')
    )
    is_successful = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.assignment.child.get_full_name()} - {self.assignment.activity.title} - {self.started_at.date()}"
    
    @property
    def percentage_score(self):
        if self.score and self.max_score:
            return round((self.score / self.max_score) * 100, 2)
        return 0


class ActivityProgress(models.Model):
    """Track overall progress for activities"""
    child = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_progress',
        limit_choices_to={'role': 'child'}
    )
    activity_type = models.CharField(
        max_length=20,
        choices=TherapyActivity.ActivityType.choices
    )
    total_attempts = models.PositiveIntegerField(default=0)
    successful_attempts = models.PositiveIntegerField(default=0)
    average_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )
    best_score = models.PositiveIntegerField(default=0)
    last_attempt_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['child', 'activity_type']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.child.get_full_name()} - {self.get_activity_type_display()}"
    
    @property
    def success_rate(self):
        if self.total_attempts > 0:
            return round((self.successful_attempts / self.total_attempts) * 100, 2)
        return 0
