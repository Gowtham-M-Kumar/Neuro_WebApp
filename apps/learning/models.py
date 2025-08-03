from django.db import models
from django.conf import settings

# Letter model (A-Z)
class Letter(models.Model):
    UPPER = 'upper'
    LOWER = 'lower'
    CASE_CHOICES = [
        (UPPER, 'Uppercase'),
        (LOWER, 'Lowercase'),
    ]
    char = models.CharField(max_length=1, unique=True)
    image = models.ImageField(upload_to='letters/')
    case = models.CharField(max_length=6, choices=CASE_CHOICES, default=UPPER)
    tracing_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.char

# Number model (0-20)
class Number(models.Model):
    value = models.PositiveSmallIntegerField(unique=True)
    image = models.ImageField(upload_to='numbers/')
    quantity_image = models.ImageField(upload_to='numbers/quantities/', blank=True, null=True)

    def __str__(self):
        return str(self.value)

# Word model (basic vocabulary)
class Word(models.Model):
    CATEGORY_CHOICES = [
        ('animal', 'Animal'),
        ('object', 'Object'),
        ('food', 'Food'),
        ('color', 'Color'),
        ('emotion', 'Emotion'),
        ('custom', 'Custom'),
    ]
    text = models.CharField(max_length=32)
    image = models.ImageField(upload_to='words/')
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.text

# Progress tracking for each module
class ChildLetterProgress(models.Model):
    child = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='letter_progress')
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    attempts = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('child', 'letter')

class ChildNumberProgress(models.Model):
    child = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='number_progress')
    number = models.ForeignKey(Number, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    attempts = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('child', 'number')

class ChildWordProgress(models.Model):
    child = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='word_progress')
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    attempts = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('child', 'word')

# Achievement/Milestone tracking
class Achievement(models.Model):
    child = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    achieved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.child} - {self.name}"
