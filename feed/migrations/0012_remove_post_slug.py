# Generated by Django 3.0.6 on 2020-05-27 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0011_post_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]