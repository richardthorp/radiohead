# Generated by Django 3.2.4 on 2021-08-06 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_album_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]