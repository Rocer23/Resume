# Generated by Django 5.2 on 2025-06-04 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_resume_address_resume_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='language',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
