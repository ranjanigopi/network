# Generated by Django 3.1.2 on 2020-11-09 17:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_follows_like_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
