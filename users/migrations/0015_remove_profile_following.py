# Generated by Django 3.0.6 on 2020-06-08 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_profile_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='following',
        ),
    ]
