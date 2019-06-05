# Generated by Django 2.1.5 on 2019-06-05 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetandeat', '0006_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='events',
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(to='meetandeat.Tag'),
        ),
    ]
