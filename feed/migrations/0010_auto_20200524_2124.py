# Generated by Django 3.0.6 on 2020-05-24 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0009_auto_20200524_2114'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
    ]