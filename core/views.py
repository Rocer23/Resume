from django.contrib.auth import login, update_session_auth_hash
from django.http import JsonResponse, FileResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib.utils import simpleSplit
from Resume.settings import FONT_PATH
from .forms import ResumeForm, NewsForm, CustomUserCreationForm, PasswordChangingForm
from django.contrib.auth.decorators import login_required
from core.models import Resume, CustomUser, News, Comment
from django.views.decorators.csrf import csrf_exempt
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# Create your views here.
def index(request):
    context = {
        'title': 'My Resume',
        'description': 'This is my Resume page.',
    }
    # show all resumes on index
    resumes = Resume.objects.all()
    other_resume = Resume.objects.all()[:10]

    # show all news on index
    news_list = News.objects.all()
    return render(request, 'index.html', {
        'context': context,
        'resumes': resumes,
        "other_resume": other_resume,
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


def change_password(request, user_id):
    if request.user.id != user_id:
        return HttpResponseForbidden("You can't change someone else's password.")

    if request.method == "POST":
        form = PasswordChangingForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('user-profile')
    else:
        form = PasswordChangingForm(user=request.user)
    return render(request, 'use_profile.html', {"form": form})


# створення резюме
@login_required(login_url="login")
def create_resume(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        try:
            user.save()
        except Exception as e:
            print(f"Помилка при збереженні користувача: {e}")

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
    resume = get_object_or_404(Resume, id=resume_id)

    if resume is None:
        return redirect('index')

    return render(request, 'resume.html', {
        'user': resume.user,
        'resume': resume,
        'title': resume.title,
        "address": resume.address,
        'phone': resume.phone,
        'description': resume.meta,
        'education': resume.education,
        'job_exp': resume.job_exp,
        "languages": resume.language,
        "skills": resume.skills,
        'add_information': resume.add_information,
    })


def download_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    FONT_NAME = 'DejaVuSans'
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
    width, height = A4

    x, y = 50, height - 50
    max_width = 480
    line_height = 16

    def write(text, size=12, bold=False, indent=0, space_before=10):
        nonlocal y
        if not text:
            return
        y -= space_before
        font = FONT_NAME + ('-Bold' if bold else "")
        p.setFont(FONT_NAME, size)
        lines = simpleSplit(str(text), FONT_NAME, size, max_width)
        for line in lines:
            if y < 50:
                p.showPage()
                y = height - 50
                p.setFont(FONT_NAME, size)
            p.drawString(x + indent, y, line)
            y -= line_height

    p.setFont(FONT_NAME, 16)
    p.drawString(x, y, f"Resume: {resume.title}")
    y -= 30

    write(f"Name: {resume.user.first_name} {resume.user.last_name}", bold=True)
    write(f"Phone: {resume.phone}")
    write(f"Address: {resume.address}")
    write(f"Languages: {resume.language}")

    write("About Me: ", bold=True, space_before=20)
    write(resume.meta)
    write(f"Job experience: ")
    write(resume.job_exp)
    write(f"Education: {resume.education}")
    write(f"Skills: {resume.skills}")
    write(f"Addition information: {resume.add_information}")

    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"{resume.title}.pdf")


def make_copy(request, resume_id):
    original = get_object_or_404(Resume, id=resume_id)
    copy_resume = Resume.objects.create(
        user=request.user,
        title=original.title,
        address=original.address,
        phone=original.phone,
        meta=original.meta,
        education=original.education,
        job_exp=original.job_exp,
        language=original.language,
        skills=original.skills,
        add_information=original.add_information
    )
    return redirect("resume", resume_id=copy_resume.id)


def edit_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    if request.method == "POST":
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'edit_resume.html', {'form': form})


def delete_resume(request, resume_id):
    resumeD = get_object_or_404(Resume, id=resume_id)
    resumeD.delete()
    return redirect("index")


@login_required(login_url='login')
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
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save()
            return redirect('news', new_id=news.id)
    else:
        form = NewsForm()
    return render(request, "create_new.html", {"form": form})


def news(request, new_id):
    news = get_object_or_404(News, id=new_id)
    comments = Comment.objects.filter(news=news).order_by('-created_at')

    return render(request, 'news.html', {
        'news': news,
        'comments': comments
    })


def news_page(request):
    news = News.objects.all()
    return render(request, "news_page.html", {
        'news': news
    })


def edit_new(request, new_id):
    news = get_object_or_404(News, id=new_id)
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news-page')
    else:
        form = NewsForm(instance=news)
    return render(request, 'edit_new.html', {'form': form})


def delete_new(request, new_id):
    newD = get_object_or_404(News, id=new_id)
    newD.delete()
    return redirect('news-page')

@csrf_exempt
@login_required(login_url="login")
def add_comment(request, new_id):
    if request.method == "POST":
        text = request.POST.get('text')

        if request.user.is_authenticated and text:

            try:
                news = News.objects.get(id=new_id)
            except News.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': "Новину не знайдено"
                })

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


def edit_comment(request, new_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, news_id=new_id)
    if request.method == "POST":
        comment.text = request.POST.get('text', '')
        comment.save()
    return redirect('news', new_id=new_id)


def delete_comment(request, new_id, comment_id):
    commentD = get_object_or_404(Comment, id=comment_id, news_id=new_id)
    commentD.delete()
    return redirect('news', new_id=new_id)
