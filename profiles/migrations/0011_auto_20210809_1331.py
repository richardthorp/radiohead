# Generated by Django 3.2.4 on 2021-08-09 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20210809_1326'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='default_street_address1',
            new_name='default_address_line1',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='default_street_address2',
            new_name='default_address_line2',
        ),
    ]