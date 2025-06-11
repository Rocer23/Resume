from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from core import views


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('create-resume/', views.create_resume, name='create_resume'),
    path('resume/<int:resume_id>/', views.resume, name='resume'),
    path('user-profile/<int:user_id>/', views.user_profile, name='user-profile'),
    path('news/', views.create_news, name="create-news"),
    path('news/<int:new_id>/', views.news, name='news'),
    path('add_comment/', views.add_comment, name='add-comment')
]
