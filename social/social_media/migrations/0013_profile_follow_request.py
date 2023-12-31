# Generated by Django 4.1.4 on 2023-03-28 11:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social_media', '0012_profile_is_private_notifaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follow_request',
            field=models.ManyToManyField(related_name='request', to=settings.AUTH_USER_MODEL),
        ),
    ]
