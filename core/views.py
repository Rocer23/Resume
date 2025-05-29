from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import ResumeForm
from django.contrib.auth.decorators import login_required
from core.models import Resume, CustomUser


# Create your views here.


def index(request):
    context = {
        'title': 'My Resume',
        'description': 'This is my Resume page.',
    }
    # show all resumes on index
    resumes = Resume.objects.all()
    return render(request, 'index.html', {
        'context': context,
        'resumes': resumes
    })


# реєстрація користувача
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, 'register.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# створення резюме
@login_required
def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('index')
    else:
        form = ResumeForm()

    return render(request, 'create_resume.html', {'form': form})


# Сторінка резюме
def resume(request, resume_id):
    try:
        resumes = Resume.objects.get(id=resume_id, user=request.user)
    except Resume.DoesNotExist:
        return redirect('resume.html')
    return render(request, 'resume.html', {'resume': resumes, 'title': resumes.title, 'description': resumes.content})


def user_profile(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect('index')
    resumes = Resume.objects.filter(user=user)
    return render(request, 'user_profile.html', {
        'user': user,
        'resumes': resumes,
        'title': f"{user.username}'s Profile",
        'description': f"Profile page of {user.username}"
    })
