from django.urls import path
from . import views

app_name = 'routines'

urlpatterns = [
    # Routine management
    path('', views.routine_list, name='routine_list'),
    path('create/', views.routine_create, name='routine_create'),
    path('<int:routine_id>/', views.routine_detail, name='routine_detail'),
    path('<int:routine_id>/edit/', views.routine_edit, name='routine_edit'),
    path('<int:routine_id>/progress/', views.routine_progress, name='routine_progress'),
    path('<int:routine_id>/schedule/', views.routine_schedule, name='routine_schedule'),
    
    # Task management
    path('<int:routine_id>/tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:task_id>/complete/', views.task_complete, name='task_complete'),
    path('tasks/reorder/', views.task_reorder, name='task_reorder'),
] 