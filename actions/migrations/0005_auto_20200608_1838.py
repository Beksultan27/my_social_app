# Generated by Django 3.0.6 on 2020-06-08 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_profile_following'),
        ('actions', '0004_auto_20200607_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='users.Profile'),
        ),
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
