# form for resume creation
from django import forms
from .models import Resume


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter resume title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter resume content', 'rows': 5}),
        }
