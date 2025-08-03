from django.urls import path
from . import views

app_name = 'drawing'

urlpatterns = [
    # Dashboard and main views
    path('', views.drawing_dashboard, name='drawing_dashboard'),
    path('list/', views.drawing_list, name='drawing_list'),
    path('analytics/', views.drawing_analytics, name='drawing_analytics'),
    
    # Canvas interface
    path('canvas/', views.drawing_canvas, name='drawing_canvas'),
    path('canvas/<int:drawing_id>/', views.drawing_canvas, name='drawing_canvas_edit'),
    
    # Drawing CRUD
    path('create/', views.DrawingCreateView.as_view(), name='drawing_create'),
    path('edit/<int:pk>/', views.DrawingUpdateView.as_view(), name='drawing_edit'),
    path('detail/<int:drawing_id>/', views.drawing_detail, name='drawing_detail'),
    path('delete/<int:drawing_id>/', views.delete_drawing, name='drawing_delete'),
    
    # AJAX endpoints for canvas operations
    path('save/<int:drawing_id>/', views.save_drawing_data, name='save_drawing_data'),
    path('load/<int:drawing_id>/', views.load_drawing_data, name='load_drawing_data'),
    path('version/<int:drawing_id>/', views.create_new_version, name='create_new_version'),
    path('session/end/<int:drawing_id>/', views.end_drawing_session, name='end_drawing_session'),
    # API endpoint for AJAX creation
    path('api/create/', views.api_create_drawing, name='api_create_drawing'),
] 