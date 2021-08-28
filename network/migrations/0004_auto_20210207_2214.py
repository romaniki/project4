# Generated by Django 3.1.6 on 2021-02-07 22:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20210207_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes_received', to=settings.AUTH_USER_MODEL),
        ),
    ]
