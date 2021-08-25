# Generated by Django 3.2.4 on 2021-08-24 18:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20210822_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='date_added',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='product',
            name='date_added',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]