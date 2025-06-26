from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import CustomUser, Resume, ResumeSection, TemplateResume, News, Comment
from core.forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'updated_at')
    search_fields = ('user__username', 'title')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(ResumeSection)
class ResumeSectionAdmin(admin.ModelAdmin):
    list_display = ('resume', 'title', 'order')
    search_fields = ('resume__title', 'title')
    list_filter = ('resume',)
    ordering = ('resume', 'order')


@admin.register(TemplateResume)
class TemplateResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'updated_at')
    search_fields = ('user__username', 'title')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'text', 'created_at')
    search_fields = ('news', 'created_at')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
