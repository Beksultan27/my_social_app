# Generated by Django 3.0.6 on 2020-06-08 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0005_auto_20200608_1838'),
        ('users', '0007_remove_profile_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='actions.Contact', to='users.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='profile_pics/'),
        ),
    ]
