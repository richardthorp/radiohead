# Generated by Django 3.2.4 on 2021-08-05 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_app', '0009_comment_edited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='single',
            name='title',
            field=models.TextField(unique=True),
        ),
    ]
