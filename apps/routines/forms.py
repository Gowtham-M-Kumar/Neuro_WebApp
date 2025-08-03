from django import forms
from django.contrib.auth import get_user_model
from .models import Routine, Task, TaskCompletion, RoutineSchedule

User = get_user_model()


class RoutineForm(forms.ModelForm):
    """Form for creating and editing routines"""
    
    class Meta:
        model = Routine
        fields = ['title', 'description', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter routine title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the routine'
            }),
            'assigned_to': forms.SelectMultiple(attrs={
                'class': 'form-select'
            })
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter assigned_to to only show children
        if user:
            self.fields['assigned_to'].queryset = User.objects.filter(role='child')
            self.fields['assigned_to'].widget.attrs.update({
                'class': 'form-select',
                'multiple': True
            })


class TaskForm(forms.ModelForm):
    """Form for creating and editing tasks"""
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'image', 'estimated_duration', 'is_required']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Describe the task'
            }),
            'estimated_duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 120,
                'placeholder': 'Duration in minutes'
            }),
            'is_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class TaskCompletionForm(forms.ModelForm):
    """Form for marking task completion"""
    
    class Meta:
        model = TaskCompletion
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Add any notes about the completion'
            })
        }


class RoutineScheduleForm(forms.ModelForm):
    """Form for scheduling routines"""
    
    class Meta:
        model = RoutineSchedule
        fields = ['routine', 'child', 'day_of_week', 'start_time', 'end_time']
        widgets = {
            'routine': forms.Select(attrs={
                'class': 'form-select'
            }),
            'child': forms.Select(attrs={
                'class': 'form-select'
            }),
            'day_of_week': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            })
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filter routines based on user role
            if user.role == 'therapist':
                self.fields['routine'].queryset = Routine.objects.filter(
                    created_by=user,
                    is_active=True
                )
            elif user.role == 'teacher':
                self.fields['routine'].queryset = Routine.objects.filter(
                    created_by=user,
                    is_active=True
                )
            elif user.role == 'parent':
                # Parents can see routines assigned to their children
                children = user.parent_profile.children.all()
                child_users = [child.user for child in children]
                self.fields['routine'].queryset = Routine.objects.filter(
                    assigned_to__in=child_users,
                    is_active=True
                ).distinct()
            
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
            elif user.role == 'parent':
                children_profiles = user.parent_profile.children.all()
                child_users = [child_profile.user for child_profile in children_profiles]
                self.fields['child'].queryset = User.objects.filter(id__in=[user.id for user in child_users])


class TaskReorderForm(forms.Form):
    """Form for reordering tasks via AJAX"""
    task_id = forms.IntegerField()
    new_order = forms.IntegerField()
    
    def clean(self):
        cleaned_data = super().clean()
        task_id = cleaned_data.get('task_id')
        new_order = cleaned_data.get('new_order')
        
        if task_id and new_order is not None:
            try:
                task = Task.objects.get(id=task_id)
                cleaned_data['task'] = task
            except Task.DoesNotExist:
                raise forms.ValidationError("Task not found")
        
        return cleaned_data 