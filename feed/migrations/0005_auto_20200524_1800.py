# Generated by Django 3.0.6 on 2020-05-24 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_auto_20200524_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default.png', upload_to='uploads/% Y/% m/% d/'),
        ),
    ]
