import io
import os.path

from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit, ImageReader
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from xhtml2pdf import pisa

from Resume import settings
from Resume.settings import FONT_PATH
from core.models import Resume, CustomUser, News, Comment
from .forms import ResumeForm, NewsForm, CustomUserCreationForm


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
    try:
        profile_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect('index')

    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_new_password')

        if new_password != confirm_password:
            return redirect('index')

        if not profile_user.check_password(current_password):
            return redirect('index')

        profile_user.set_password(new_password)
        profile_user.save()
        update_session_auth_hash(request, profile_user)

    return redirect('index')


# створення резюме
@login_required(login_url="login")
def create_resume(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        try:
            user.save()
        except Exception as e:
            print(f"Помилка при збереженні користувача: {e}")

        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('index')
    else:
        form = ResumeForm(initial={
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email
        })

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
        'user_picture': resume.user_picture,
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
    width, height = A4
    margin = 50

    FONT_NAME = 'DejaVuSans'
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
    p.setFont(FONT_NAME, 12)


    x_left = margin
    x_right = width / 2 + 10
    y = height - margin

    if resume.user_picture:
        image_path = os.path.join(settings.MEDIA_ROOT, str(resume.user_picture))
        if os.path.exists(image_path):
            try:
                img = ImageReader(image_path)
                img_width = 100
                img_height = 100
                p.drawImage(img, x_left, y - img_height, width=img_width, height=img_height, mask='auto')
                y -= img_height + 10
            except Exception as e:
                print(f"Image error: {e}") 

    p.setFont(FONT_NAME, 16)
    p.setFillColor(HexColor("#000000"))
    p.drawString(x_right, height - margin, f"{resume.user.first_name} {resume.user.last_name}")

    p.setFont(FONT_NAME, 12)
    if resume.title:
        p.drawString(x_right, height - margin - 20, f"{resume.title}")

    contact_y = y - 10
    p.setFont(FONT_NAME, 10)
    p.drawString(x_left, contact_y, f"Phone: {resume.phone}")
    p.drawString(x_left, contact_y - 15, f"Email: {resume.user.email}")
    p.drawString(x_left, contact_y - 30, f"Address: {resume.address}")
    y = contact_y - 50

    def section_of_write(title, content):
        nonlocal y
        if not content:
            return
        if y < 100:
            p.showPage()
            y = height - margin
        p.setFont(FONT_NAME, 13)
        p.setFillColor(HexColor("#005f73"))
        p.drawString(x_left, y, title)
        y -= 20
        p.setFont(FONT_NAME, 11)
        p.setFillColor(HexColor("#000000"))
        lines = simpleSplit(str(content), FONT_NAME, 11, width - 2 * margin)

        for line in lines:
            if y < 50:
                p.showPage()
                y = height - margin
            p.drawString(x_left, y, line)
            y -= 15
        y -= 10
    
    section_of_write("About Me", resume.meta)
    section_of_write("Skills", resume.skills)
    section_of_write("Expirience", resume.job_exp)
    section_of_write("Education", resume.education)
    section_of_write("Additional Info", resume.add_information)


    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"{resume.title}.pdf")

def make_copy(request, resume_id):
    original = get_object_or_404(Resume, id=resume_id)
    copy_resume = Resume.objects.create(
        user=request.user,
        user_picture=original.user_picture,
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
        form = ResumeForm(request.POST, request.FILES, instance=resume)
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
        profile_user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect('index')

    if request.user != profile_user:
        return redirect('index')

    if request.method == "POST":
        profile_user.first_name = request.POST.get('first_name', '').strip()
        profile_user.last_name = request.POST.get('last_name', '').strip()
        profile_user.save()
        return redirect('user-profile', user_id=profile_user.id)

    resumes = Resume.objects.filter(user=profile_user)
    return render(request, 'user_profile.html', {
        'profile_user': profile_user,
        'resumes': resumes,
        'title': f"{profile_user.username}'s Profile",
        'description': f"Profile page of {profile_user.username}"
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
