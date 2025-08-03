from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Custom user model with role-based access"""
    
    class UserRole(models.TextChoices):
        PARENT = 'parent', _('Parent')
        THERAPIST = 'therapist', _('Therapist')
        TEACHER = 'teacher', _('Teacher')
        CHILD = 'child', _('Child')
    
    # Override email to be unique and required
    email = models.EmailField(_('email address'), unique=True)
    
    # Add role field
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.PARENT,
        help_text=_('User role in the system')
    )
    
    # Override username to use email
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    
    # Additional fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Use email as username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email


class ParentProfile(models.Model):
    """Profile for parent users"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='parent_profile')
    children = models.ManyToManyField('ChildProfile', related_name='parents', blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Parent: {self.user.get_full_name()}"


class TherapistProfile(models.Model):
    """Profile for therapist users"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='therapist_profile')
    license_number = models.CharField(max_length=50, blank=True, null=True)
    specializations = models.TextField(blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    assigned_children = models.ManyToManyField('ChildProfile', related_name='therapists', blank=True)
    
    def __str__(self):
        return f"Therapist: {self.user.get_full_name()}"


class TeacherProfile(models.Model):
    """Profile for teacher users"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    classroom_info = models.CharField(max_length=100, blank=True, null=True)
    grade_level = models.CharField(max_length=20, blank=True, null=True)
    assigned_children = models.ManyToManyField('ChildProfile', related_name='teachers', blank=True)
    
    def __str__(self):
        return f"Teacher: {self.user.get_full_name()}"


class ChildProfile(models.Model):
    """Profile for child users"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='child_profile')
    age = models.PositiveIntegerField()
    diagnosis_info = models.TextField(blank=True, null=True)
    learning_level = models.CharField(max_length=20, default='beginner')
    primary_parent = models.ForeignKey(ParentProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='primary_children')
    primary_therapist = models.ForeignKey(TherapistProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='primary_children')
    primary_teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='primary_children')
    
    def __str__(self):
        return f"Child: {self.user.get_full_name()}"
    
    @property
    def full_name(self):
        return self.user.get_full_name()
