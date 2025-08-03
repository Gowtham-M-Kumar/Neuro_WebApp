from django.urls import path
from . import views

app_name = 'therapy'

urlpatterns = [
    # Activity management
    path('', views.activity_list, name='activity_list'),
    path('create/', views.activity_create, name='activity_create'),
    path('<int:activity_id>/', views.activity_detail, name='activity_detail'),
    path('<int:activity_id>/edit/', views.activity_edit, name='activity_edit'),
    path('<int:activity_id>/assign/', views.activity_assign, name='activity_assign'),
    
    # Item management
    path('<int:activity_id>/items/create/', views.item_create, name='item_create'),
    path('items/<int:item_id>/edit/', views.item_edit, name='item_edit'),
    
    # Activity interaction
    path('assignments/<int:assignment_id>/play/', views.activity_play, name='activity_play'),
    path('assignments/<int:assignment_id>/submit/', views.activity_submit, name='activity_submit'),
    
    # Progress tracking
    path('progress/', views.progress_report, name='progress_report'),
    path('games/', views.game_dashboard, name='game_dashboard'),
] 