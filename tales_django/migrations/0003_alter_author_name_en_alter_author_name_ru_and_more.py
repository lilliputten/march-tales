# Generated by Django 5.0 on 2025-03-13 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tales_django', '0002_alter_track_audio_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='name_en',
            field=models.TextField(max_length=256, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='author',
            name='name_ru',
            field=models.TextField(max_length=256, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='author',
            name='short_description_en',
            field=models.TextField(blank=True, max_length=512, verbose_name='short description'),
        ),
        migrations.AlterField(
            model_name='author',
            name='short_description_ru',
            field=models.TextField(blank=True, max_length=512, verbose_name='short description'),
        ),
        migrations.AlterField(
            model_name='rubric',
            name='text_en',
            field=models.TextField(max_length=256, verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='rubric',
            name='text_ru',
            field=models.TextField(max_length=256, verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='text_en',
            field=models.TextField(max_length=256, verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='text_ru',
            field=models.TextField(max_length=256, verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='track',
            name='description_en',
            field=models.TextField(blank=True, help_text='Optional description', max_length=1024, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='track',
            name='description_ru',
            field=models.TextField(blank=True, help_text='Optional description', max_length=1024, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='track',
            name='title_en',
            field=models.TextField(help_text='The track title text, required.', max_length=256, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='track',
            name='title_ru',
            field=models.TextField(help_text='The track title text, required.', max_length=256, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='track',
            name='youtube_url',
            field=models.URLField(blank=True, help_text='YouTube video link url', max_length=64, verbose_name='youtube link'),
        ),
    ]
