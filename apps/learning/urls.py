from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.learning_dashboard, name='learning_dashboard'),
    path('alphabet/', views.alphabet_learning, name='alphabet_learning'),
    path('alphabet/<str:letter>/', views.letter_detail, name='letter_detail'),
    path('numbers/', views.number_learning, name='number_learning'),
    path('numbers/<int:number>/', views.number_detail, name='number_detail'),
    path('words/', views.word_learning, name='word_learning'),
    path('words/<int:word_id>/', views.word_detail, name='word_detail'),
    path('progress/', views.progress_dashboard, name='progress_dashboard'),
] 