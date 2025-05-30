# Generated by Django 5.0 on 2025-04-08 13:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tales_django', '0014_author_published_at_author_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='played_count',
            field=models.BigIntegerField(default=0, verbose_name='Played count'),
        ),
        migrations.CreateModel(
            name='UserTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_favorite', models.BooleanField(default=False, help_text='Is track in favorites for the current user?', verbose_name='Is favorite')),
                ('favorited_at', models.DateTimeField(help_text='When track was added/removed to/from favorites', null=True, verbose_name='Added to favorites')),
                ('played_count', models.BigIntegerField(default=0, help_text='Played count by this user', verbose_name='Played count')),
                ('position', models.FloatField(default=0, help_text='Last playback position (seconds)', verbose_name='Playback position')),
                ('played_at', models.DateTimeField(help_text='Last played time', null=True, verbose_name='Last played')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track_user_relation', to='tales_django.track', verbose_name='Track')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_track_relation', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'user track',
                'verbose_name_plural': 'user tracks',
            },
        ),
    ]
