# Generated by Django 5.1.3 on 2024-11-24 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teacherportal", "0007_remove_attendance_teacher_resource"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance",
            name="teacher",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="teacherportal.teacher",
            ),
        ),
    ]
