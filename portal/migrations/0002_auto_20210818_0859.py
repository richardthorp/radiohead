# Generated by Django 3.2.4 on 2021-08-18 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='portalimagespost',
            name='slug',
            field=models.SlugField(default=''),
        ),
        migrations.AddField(
            model_name='portaltextpost',
            name='slug',
            field=models.SlugField(default=''),
        ),
        migrations.AddField(
            model_name='portalvideopost',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
