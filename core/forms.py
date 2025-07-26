# form for resume creation
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
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
        fields = ['user_picture', 'title', 'meta', 'phone', 'address', 'language', 'skills', 'education', 'job_exp',
                  'add_information']
        widgets = {
            'user_picture': forms.FileInput(attrs={'class': "form-control photo-upload"}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter resume title'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'meta': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Enter resume content', 'rows': 5}),
            'education': forms.Textarea(attrs={'class': "form-control", 'placeholder': "Enter your education"}),
            'job_exp': forms.Textarea(attrs={'class': 'form-control', "placeholder": "Enter your job experience"}),
            'language': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Enter languages"}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Enter your skills"}),
            "add_information": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Add information about you"}),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'picture']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': "form-control photo-upload"})
        }


#Form for changing password
class ChangingPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter old password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Enter new password"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Enter new password again"}))

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')