# Generated by Django 3.2.4 on 2021-07-05 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pics/default_profile_pic.jpg', null=True, upload_to='profile_pics'),
        ),
    ]
