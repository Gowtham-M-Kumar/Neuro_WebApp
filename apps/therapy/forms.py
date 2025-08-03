from django import forms
from django.contrib.auth import get_user_model
from .models import (
    TherapyActivity, ActivityItem, ActivityAssignment, 
    ActivityAttempt, ActivityProgress
)

User = get_user_model()


class TherapyActivityForm(forms.ModelForm):
    """Form for creating and editing therapy activities"""
    
    class Meta:
        model = TherapyActivity
        fields = ['title', 'description', 'activity_type', 'difficulty_level', 'instructions']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter activity title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the activity'
            }),
            'activity_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'difficulty_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Instructions for the child'
            })
        }


class ActivityItemForm(forms.ModelForm):
    """Form for creating and editing activity items"""
    
    class Meta:
        model = ActivityItem
        fields = ['title', 'image', 'audio_file', 'order', 'is_correct_answer', 'group_id']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter item title'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'audio_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'audio/*'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_correct_answer': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'group_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Group ID for related items'
            })
        }


class ActivityAssignmentForm(forms.ModelForm):
    """Form for assigning activities to children"""
    
    class Meta:
        model = ActivityAssignment
        fields = ['activity', 'child', 'due_date', 'notes']
        widgets = {
            'activity': forms.Select(attrs={
                'class': 'form-select'
            }),
            'child': forms.Select(attrs={
                'class': 'form-select'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Add any notes for this assignment'
            })
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filter activities based on user role
            if user.role == 'therapist':
                self.fields['activity'].queryset = TherapyActivity.objects.filter(
                    created_by=user,
                    is_active=True
                )
            elif user.role == 'teacher':
                self.fields['activity'].queryset = TherapyActivity.objects.filter(
                    created_by=user,
                    is_active=True
                )
            
            # Filter children based on user role
            if user.role == 'therapist':
                self.fields['child'].queryset = User.objects.filter(
                    role='child',
                    therapist_profile__therapists=user.therapist_profile
                )
            elif user.role == 'teacher':
                self.fields['child'].queryset = User.objects.filter(
                    role='child',
                    teacher_profile__teachers=user.teacher_profile
                )


class ActivityAttemptForm(forms.ModelForm):
    """Form for recording activity attempts"""
    
    class Meta:
        model = ActivityAttempt
        fields = ['score', 'max_score', 'time_taken', 'is_successful', 'notes']
        widgets = {
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Score achieved'
            }),
            'max_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Maximum possible score'
            }),
            'time_taken': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Time taken in seconds'
            }),
            'is_successful': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Add any notes about this attempt'
            })
        }


class ActivityFilterForm(forms.Form):
    """Form for filtering activities"""
    activity_type = forms.ChoiceField(
        choices=[('', 'All Types')] + TherapyActivity.ActivityType.choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    difficulty_level = forms.ChoiceField(
        choices=[('', 'All Levels')] + TherapyActivity.DifficultyLevel.choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    is_active = forms.ChoiceField(
        choices=[('', 'All'), ('True', 'Active'), ('False', 'Inactive')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search activities...'
        })
    )


class ProgressFilterForm(forms.Form):
    """Form for filtering progress reports"""
    activity_type = forms.ChoiceField(
        choices=[('', 'All Types')] + TherapyActivity.ActivityType.choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    ) 