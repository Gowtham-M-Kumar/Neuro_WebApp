from django.contrib import admin
from .models import Letter, Number, Word, ChildLetterProgress, ChildNumberProgress, ChildWordProgress, Achievement

# Register your models here.

admin.site.register(Letter)
admin.site.register(Number)
admin.site.register(Word)
admin.site.register(ChildLetterProgress)
admin.site.register(ChildNumberProgress)
admin.site.register(ChildWordProgress)
admin.site.register(Achievement)
