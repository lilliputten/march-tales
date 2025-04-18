# Generated by Django 5.0 on 2025-04-02 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tales_django', '0011_alter_track_audio_duration_alter_track_audio_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='promote',
            field=models.BooleanField(default=True, help_text='Promote on the main page', verbose_name='Promote'),
        ),
        migrations.AlterField(
            model_name='rubric',
            name='promote',
            field=models.BooleanField(default=True, help_text='Promote on the main page', verbose_name='Promote'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='promote',
            field=models.BooleanField(default=True, help_text='Promote on the main page', verbose_name='Promote'),
        ),
    ]
