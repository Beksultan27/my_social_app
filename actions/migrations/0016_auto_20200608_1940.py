# Generated by Django 3.0.6 on 2020-06-08 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_profile_following'),
        ('actions', '0015_auto_20200608_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='user_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_from_set', to='users.Profile'),
        ),
    ]