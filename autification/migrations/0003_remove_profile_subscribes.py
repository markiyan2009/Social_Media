# Generated by Django 5.1.1 on 2024-11-21 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autification', '0002_alter_profile_about_user_alter_profile_subscribes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='subscribes',
        ),
    ]
