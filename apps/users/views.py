from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, ParentProfileForm,
    TherapistProfileForm, TeacherProfileForm, ChildProfileForm, UserProfileForm
)
from .models import CustomUser, ParentProfile, TherapistProfile, TeacherProfile, ChildProfile


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('users:dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('users:login')


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email  # Set username to email
            user.save()
            
            # Create profile based on role
            role = user.role
            if role == CustomUser.UserRole.PARENT:
                ParentProfile.objects.create(user=user)
            elif role == CustomUser.UserRole.THERAPIST:
                TherapistProfile.objects.create(user=user)
            elif role == CustomUser.UserRole.TEACHER:
                TeacherProfile.objects.create(user=user)
            elif role == CustomUser.UserRole.CHILD:
                ChildProfile.objects.create(user=user, age=5)  # Default age
            
            # Log the user in
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.get_full_name()}.')
            return redirect('users:dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def dashboard_view(request):
    """Role-based dashboard view"""
    user = request.user
    
    context = {
        'user': user,
    }
    
    # Add role-specific context
    if user.role == CustomUser.UserRole.PARENT:
        try:
            parent_profile = user.parent_profile
            context['children'] = parent_profile.children.all()
            context['profile'] = parent_profile
        except ParentProfile.DoesNotExist:
            pass
    
    elif user.role == CustomUser.UserRole.THERAPIST:
        try:
            therapist_profile = user.therapist_profile
            context['assigned_children'] = therapist_profile.assigned_children.all()
            context['profile'] = therapist_profile
        except TherapistProfile.DoesNotExist:
            pass
    
    elif user.role == CustomUser.UserRole.TEACHER:
        try:
            teacher_profile = user.teacher_profile
            context['assigned_children'] = teacher_profile.assigned_children.all()
            context['profile'] = teacher_profile
        except TeacherProfile.DoesNotExist:
            pass
    
    elif user.role == CustomUser.UserRole.CHILD:
        try:
            child_profile = user.child_profile
            context['profile'] = child_profile
        except ChildProfile.DoesNotExist:
            pass
    
    return render(request, f'users/dashboard_{user.role}.html', context)


@login_required
def profile_view(request):
    """User profile view and edit"""
    user = request.user
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)
        
        # Get the appropriate profile form based on user role
        if user.role == CustomUser.UserRole.PARENT:
            try:
                profile = user.parent_profile
                profile_form = ParentProfileForm(request.POST, instance=profile)
            except ParentProfile.DoesNotExist:
                profile = ParentProfile.objects.create(user=user)
                profile_form = ParentProfileForm(request.POST, instance=profile)
        elif user.role == CustomUser.UserRole.THERAPIST:
            try:
                profile = user.therapist_profile
                profile_form = TherapistProfileForm(request.POST, instance=profile)
            except TherapistProfile.DoesNotExist:
                profile = TherapistProfile.objects.create(user=user)
                profile_form = TherapistProfileForm(request.POST, instance=profile)
        elif user.role == CustomUser.UserRole.TEACHER:
            try:
                profile = user.teacher_profile
                profile_form = TeacherProfileForm(request.POST, instance=profile)
            except TeacherProfile.DoesNotExist:
                profile = TeacherProfile.objects.create(user=user)
                profile_form = TeacherProfileForm(request.POST, instance=profile)
        elif user.role == CustomUser.UserRole.CHILD:
            try:
                profile = user.child_profile
                profile_form = ChildProfileForm(request.POST, instance=profile)
            except ChildProfile.DoesNotExist:
                profile = ChildProfile.objects.create(user=user, age=5)  # Default age
                profile_form = ChildProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
    else:
        user_form = UserProfileForm(instance=user)
        
        # Get the appropriate profile form based on user role
        if user.role == CustomUser.UserRole.PARENT:
            try:
                profile = user.parent_profile
                profile_form = ParentProfileForm(instance=profile)
            except ParentProfile.DoesNotExist:
                profile = ParentProfile.objects.create(user=user)
                profile_form = ParentProfileForm(instance=profile)
        elif user.role == CustomUser.UserRole.THERAPIST:
            try:
                profile = user.therapist_profile
                profile_form = TherapistProfileForm(instance=profile)
            except TherapistProfile.DoesNotExist:
                profile = TherapistProfile.objects.create(user=user)
                profile_form = TherapistProfileForm(instance=profile)
        elif user.role == CustomUser.UserRole.TEACHER:
            try:
                profile = user.teacher_profile
                profile_form = TeacherProfileForm(instance=profile)
            except TeacherProfile.DoesNotExist:
                profile = TeacherProfile.objects.create(user=user)
                profile_form = TeacherProfileForm(instance=profile)
        elif user.role == CustomUser.UserRole.CHILD:
            try:
                profile = user.child_profile
                profile_form = ChildProfileForm(instance=profile)
            except ChildProfile.DoesNotExist:
                profile = ChildProfile.objects.create(user=user, age=5)  # Default age
                profile_form = ChildProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user,
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def user_list_view(request):
    """View for listing users (for admin/staff)"""
    if not request.user.is_staff and request.user.role not in ['therapist', 'teacher']:
        messages.error(request, 'Access denied.')
        return redirect('users:dashboard')
    
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def user_detail_view(request, user_id):
    """View for user details (for admin/staff)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('users:dashboard')
    
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'users/user_detail.html', {'user_detail': user})
