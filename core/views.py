from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ResumeForm, NewsForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from core.models import Resume, CustomUser, News, Comment
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def index(request):
    context = {
        'title': 'My Resume',
        'description': 'This is my Resume page.',
    }
    # show all resumes on index
    resumes = Resume.objects.all()

    # show all news on index
    news_list = News.objects.all()
    return render(request, 'index.html', {
        'context': context,
        'resumes': resumes,
        'news_list': news_list,
    })


# реєстрація користувача
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
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
        user = resumes.user
    except Resume.DoesNotExist:
        return redirect('index')
    return render(request, 'resume.html', {
        'user': user,
        'resume': resumes,
        'title': resumes.title,
        'description': resumes.content,
        'phone': resumes.phone,
        "address": resumes.address,
        "languages": resumes.language
    })


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


def create_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            return redirect('news', {'news': news})
    else:
        form = NewsForm()
    return render(request, "create_new.html", {"form": form})


def news(request, new_id):
    try:
        news = get_object_or_404(News, id=new_id)
        comments = Comment.objects.filter(news=news).order_by('-created_at')
    except News.DoesNotExist:
        return redirect('index')
    return render(request, 'news.html', {
        'news': news,
        'comments': comments
    })


@csrf_exempt
def add_comment(request):
    if request.method == "POST":
        news_id = request.POST.get('news_id')
        text = request.POST.get('text')

        if request.user.is_authenticated and news_id and text:
            news = News.objects.get(id=news_id)
            comment = Comment.objects.create(
                username=request.user,
                news=news,
                text=text
            )
            return JsonResponse({
                'status': 'ok',
                'username': request.user.username,
                'text': comment.text,
                'create_at': comment.created_at.strftime("%d.%m.%Y %H:%M")
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Недійсні дані або неавторизований користувач'
            })
    return JsonResponse({
        'status': 'error',
        'message': 'Невірний метод'
    })
