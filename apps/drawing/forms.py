from django import forms
from .models import Drawing


class DrawingForm(forms.ModelForm):
    """Form for creating and updating drawings"""
    
    class Meta:
        model = Drawing
        fields = ['title', 'shared_with_parents', 'shared_with_therapists', 'shared_with_teachers']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter drawing title...'
            }),
            'shared_with_parents': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'shared_with_therapists': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'shared_with_teachers': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make title required
        self.fields['title'].required = True 