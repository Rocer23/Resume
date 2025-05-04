from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    """
    Custom user model that extends AbstractUser.
    """
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Resume(models.Model):
    """
    Model representing a resume.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    is_template = models.BooleanField(default=False)
    template_name = models.CharField(max_length=255, blank=True, null=True)
    template_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.user}"


class Resume_sections(models.Model):
    """
    Model representing sections of a resume.
    """
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=50, choices=[
        ('education', 'Education'),
        ('experience', 'Experience'),
        ('skills', 'Skills'),
        ('projects', 'Projects'),
        ('certifications', 'Certifications'),
        ('languages', 'languages'),
        ('references', 'References'),
        ('summary', 'Summary'),
        ('objective', 'Objective'),
        ('awards', 'Awards'),
        ('publications', 'Publications'),
        ('volunteer', 'Volunteer'),
        ('hobbies', 'Hobbies'),
        ('interests', 'Interests'),
    ])
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.JSONField(blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=True)
    is_template = models.BooleanField(default=False)
    template_name = models.CharField(max_length=255, blank=True, null=True)
    template_data = models.JSONField(blank=True, null=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.section_type} - {self.resume.name}"


class Resume_template(models.Model):
    """
    Model representing a resume template.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    template_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.description}"


class News(models.Model):
    """
    Model representing news articles.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.created_at}"
