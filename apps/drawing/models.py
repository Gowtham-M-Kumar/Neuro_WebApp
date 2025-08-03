from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import json


class Drawing(models.Model):
    """Model to store drawing data and metadata"""
    
    title = models.CharField(max_length=200, default="Untitled Drawing")
    child = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='drawings',
        limit_choices_to={'role': 'child'}
    )
    
    # Canvas data storage
    canvas_data = models.JSONField(default=dict, help_text="Serialized canvas drawing data")
    canvas_width = models.PositiveIntegerField(default=800)
    canvas_height = models.PositiveIntegerField(default=600)
    
    # Drawing metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    
    # Sharing permissions
    shared_with_parents = models.BooleanField(default=True)
    shared_with_therapists = models.BooleanField(default=True)
    shared_with_teachers = models.BooleanField(default=True)
    
    # Version control
    parent_drawing = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='versions'
    )
    version_number = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('drawing')
        verbose_name_plural = _('drawings')
    
    def __str__(self):
        return f"{self.title} by {self.child.get_full_name()}"
    
    def save(self, *args, **kwargs):
        # Auto-increment version number for new versions
        if self.parent_drawing and not self.pk:
            latest_version = Drawing.objects.filter(
                parent_drawing=self.parent_drawing
            ).order_by('-version_number').first()
            self.version_number = (latest_version.version_number + 1) if latest_version else 2
        super().save(*args, **kwargs)
    
    def get_canvas_data(self):
        """Return canvas data as a dictionary"""
        if isinstance(self.canvas_data, str):
            return json.loads(self.canvas_data)
        return self.canvas_data or {}
    
    def set_canvas_data(self, data):
        """Set canvas data from dictionary"""
        self.canvas_data = data
    
    def create_new_version(self):
        """Create a new version of this drawing"""
        new_drawing = Drawing.objects.create(
            title=self.title,
            child=self.child,
            canvas_data=self.canvas_data,
            canvas_width=self.canvas_width,
            canvas_height=self.canvas_height,
            parent_drawing=self.parent_drawing or self,
            shared_with_parents=self.shared_with_parents,
            shared_with_therapists=self.shared_with_therapists,
            shared_with_teachers=self.shared_with_teachers,
        )
        return new_drawing
    
    def can_be_viewed_by(self, user):
        """Check if user can view this drawing"""
        if user == self.child:
            return True
        
        if user.role == 'parent' and self.shared_with_parents:
            return user.parent_profile.children.filter(user=self.child).exists()
        
        if user.role == 'therapist' and self.shared_with_therapists:
            return user.therapist_profile.assigned_children.filter(user=self.child).exists()
        
        if user.role == 'teacher' and self.shared_with_teachers:
            return user.teacher_profile.assigned_children.filter(user=self.child).exists()
        
        return False


class DrawingSession(models.Model):
    """Model to track drawing sessions for analytics"""
    
    drawing = models.ForeignKey(Drawing, on_delete=models.CASCADE, related_name='sessions')
    child = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    
    # Session analytics
    strokes_count = models.PositiveIntegerField(default=0)
    colors_used = models.JSONField(default=list)
    tools_used = models.JSONField(default=list)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Drawing session for {self.drawing.title} by {self.child.get_full_name()}"
    
    def end_session(self, duration_seconds=None):
        """End the drawing session"""
        from django.utils import timezone
        self.ended_at = timezone.now()
        if duration_seconds:
            self.duration_seconds = duration_seconds
        else:
            self.duration_seconds = int((self.ended_at - self.started_at).total_seconds())
        self.save()
