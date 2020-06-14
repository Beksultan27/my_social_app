# Generated by Django 3.0.6 on 2020-06-08 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('actions', '0011_auto_20200608_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='user_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_from_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
