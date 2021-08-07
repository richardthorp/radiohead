# Generated by Django 3.2.4 on 2021-08-07 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_profile_default_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='default_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
