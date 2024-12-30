# Generated by Django 5.1.1 on 2024-12-26 07:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0009_remove_community_subscribers_community_subscribers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='community',
            old_name='genres',
            new_name='genre',
        ),
        migrations.AlterField(
            model_name='community',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscribers', to=settings.AUTH_USER_MODEL),
        ),
    ]
