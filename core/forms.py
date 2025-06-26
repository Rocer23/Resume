# form for resume creation
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Resume, News, CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff')


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'content', 'phone', 'address', 'language', 'skills']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter resume title'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Enter resume content', 'rows': 5}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'language': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Enter languages"}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Enter your skills"}),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'picture']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }
