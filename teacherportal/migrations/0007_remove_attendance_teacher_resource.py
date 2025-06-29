# Generated by Django 5.1.3 on 2024-11-24 17:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teacherportal", "0006_attendance_teacher"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attendance",
            name="teacher",
        ),
        migrations.CreateModel(
            name="Resource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("file", models.FileField(upload_to="resources/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resources",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
