# Generated by Django 3.2.4 on 2021-08-18 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_auto_20210818_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='portalimagespost',
            name='post_blurb',
            field=models.CharField(default='blurb', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='portaltextpost',
            name='post_blurb',
            field=models.CharField(default='blurb', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='portalvideopost',
            name='post_blurb',
            field=models.CharField(default='blurb', max_length=250),
            preserve_default=False,
        ),
    ]
