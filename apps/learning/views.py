from django.shortcuts import render, get_object_or_404
from .models import Letter, Number, Word, ChildLetterProgress, ChildNumberProgress, ChildWordProgress, Achievement
from django.contrib.auth.decorators import login_required

@login_required
def alphabet_learning(request):
    letters = Letter.objects.all().order_by('char')
    return render(request, 'learning/alphabet_learning.html', {'letters': letters})

@login_required
def letter_detail(request, letter):
    letter_obj = get_object_or_404(Letter, char__iexact=letter)
    return render(request, 'learning/letter_detail.html', {'letter': letter_obj})

@login_required
def number_learning(request):
    numbers = Number.objects.all().order_by('value')
    return render(request, 'learning/number_learning.html', {'numbers': numbers})

@login_required
def number_detail(request, number):
    number_obj = get_object_or_404(Number, value=number)
    return render(request, 'learning/number_detail.html', {'number': number_obj})

@login_required
def word_learning(request):
    categories = Word.CATEGORY_CHOICES
    return render(request, 'learning/word_learning.html', {'categories': categories})

@login_required
def word_detail(request, word_id):
    word_obj = get_object_or_404(Word, id=word_id)
    return render(request, 'learning/word_detail.html', {'word': word_obj})

@login_required
def progress_dashboard(request):
    return render(request, 'learning/progress_dashboard.html')

def learning_dashboard(request):
    return render(request, 'learning/dashboard.html')
