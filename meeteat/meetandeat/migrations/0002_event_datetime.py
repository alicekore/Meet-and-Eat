# Generated by Django 2.1.7 on 2019-05-26 17:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meetandeat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
