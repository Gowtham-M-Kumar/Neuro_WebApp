from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, ParentProfile, TherapistProfile, TeacherProfile, ChildProfile


class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users with role-based fields"""
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'role')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'register-input'}),
            'last_name': forms.TextInput(attrs={'class': 'register-input'}),
            'email': forms.EmailInput(attrs={'class': 'register-input'}),
            'role': forms.Select(attrs={'class': 'register-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'register-input'})
        self.fields['password2'].widget.attrs.update({'class': 'register-input'})


class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form using email"""
    
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'login-input'})
        self.fields['password'].widget.attrs.update({'class': 'login-input'})


class ParentProfileForm(forms.ModelForm):
    """Form for parent profile creation/editing"""
    
    class Meta:
        model = ParentProfile
        fields = ('emergency_contact', 'address')
        widgets = {
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TherapistProfileForm(forms.ModelForm):
    """Form for therapist profile creation/editing"""
    
    class Meta:
        model = TherapistProfile
        fields = ('license_number', 'specializations', 'years_of_experience')
        widgets = {
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'specializations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TeacherProfileForm(forms.ModelForm):
    """Form for teacher profile creation/editing"""
    
    class Meta:
        model = TeacherProfile
        fields = ('classroom_info', 'grade_level')
        widgets = {
            'classroom_info': forms.TextInput(attrs={'class': 'form-control'}),
            'grade_level': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ChildProfileForm(forms.ModelForm):
    """Form for child profile creation/editing"""
    
    class Meta:
        model = ChildProfile
        fields = ('age', 'diagnosis_info', 'learning_level')
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'diagnosis_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'learning_level': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('beginner', 'Beginner'),
                ('intermediate', 'Intermediate'),
                ('advanced', 'Advanced'),
            ]),
        }


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information"""
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'profile_picture')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        } 