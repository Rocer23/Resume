# form for resume creation
from django import forms
from .models import Resume, News


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'content', 'phone', 'address', 'language']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter resume title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter resume content', 'rows': 5}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'language': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Enter languages"})
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }
