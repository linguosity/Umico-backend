# Generated by Django 5.0.6 on 2024-05-27 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("umico_app", "0005_frame_mat_in_total_frame_mat_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="scan",
            name="job_notes",
            field=models.TextField(default="No notes at this time"),
        ),
    ]
