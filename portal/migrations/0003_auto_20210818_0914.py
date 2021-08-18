# Generated by Django 3.2.4 on 2021-08-18 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_auto_20210818_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='portalimagespost',
            name='images',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AddField(
            model_name='portaltextpost',
            name='text',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AddField(
            model_name='portalvideopost',
            name='video',
            field=models.BooleanField(default=True, editable=False),
        ),
    ]