# Generated by Django 3.2.4 on 2021-08-12 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_auto_20210809_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='portal_cust_id',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='profile',
            name='subscription_id',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='profile',
            name='subscription_status',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
