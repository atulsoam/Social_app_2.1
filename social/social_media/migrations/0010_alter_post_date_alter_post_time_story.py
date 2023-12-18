# Generated by Django 4.1.4 on 2023-03-24 07:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social_media', '0009_comment_profiles_alter_post_date_alter_post_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.TimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story', models.ImageField(upload_to='social_media/pictures/story')),
                ('date_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('likes', models.ManyToManyField(related_name='story_like', to=settings.AUTH_USER_MODEL)),
                ('profiles', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storyprofile', to='social_media.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storyusers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]