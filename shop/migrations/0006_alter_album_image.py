# Generated by Django 3.2.4 on 2021-06-27 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210627_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='image',
            field=models.ImageField(upload_to='album_covers/'),
        ),
    ]
