from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from core.models import Resume


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
        'resumes' : resumes
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
def create_resume(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        # Тут можна зберегти резюме у базу даних
        resume = Resume(title=title, content=content)
        resume.save()
        return redirect('index')

    return render(request, 'create_resume.html')
