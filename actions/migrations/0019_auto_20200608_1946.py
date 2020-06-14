# Generated by Django 3.0.6 on 2020-06-08 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_remove_profile_following'),
        ('actions', '0018_auto_20200608_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='user_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_from_set', to='users.Profile'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='user_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_to_set', to='users.Profile'),
        ),
    ]
