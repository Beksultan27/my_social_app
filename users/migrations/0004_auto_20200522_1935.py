# Generated by Django 3.0.6 on 2020-05-22 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200522_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(default=None, max_length=80),
        ),
    ]
