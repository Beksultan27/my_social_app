# Generated by Django 3.0.6 on 2020-06-06 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0017_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='total_likes',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]
