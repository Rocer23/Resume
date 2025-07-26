from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path('resume/<uuid:resume_id>/', views.resume, name='resume'),
    path('resume/<uuid:resume_id>/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<uuid:resume_id>/copy/', views.make_copy, name="copy-resume"),
    path('resume/<uuid:resume_id>/download/', views.download_resume, name='download-resume'),
    path('resume/<uuid:resume_id>/delete/', views.delete_resume, name='delete_resume'),
    path('user-profile/<uuid:user_id>/', views.user_profile, name='user-profile'),
    path('user-profile/<uuid:user_id>/change-password/', views.change_password, name='change-password'),
    path('create-news/', views.create_news, name="create-news"),
    path('news-page/', views.news_page, name='news-page'),
    path('news/<uuid:new_id>/', views.news, name='news'),
    path('news/<uuid:new_id>/edit/', views.edit_new, name='edit-new'),
    path('news/<uuid:new_id>/delete/', views.delete_new, name="delete-new"),
    path('news/<uuid:new_id>/add_comment/', views.add_comment, name='add_comment'),
    path('news/<uuid:new_id>/edit_comment/<uuid:comment_id>/', views.edit_comment, name='edit_comment'),
    path('news/<uuid:new_id>/delete_comment/<uuid:comment_id>/', views.delete_comment, name='delete_comment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
