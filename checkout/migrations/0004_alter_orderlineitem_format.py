# Generated by Django 3.2.4 on 2021-08-03 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20210802_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlineitem',
            name='format',
            field=models.CharField(blank=True, choices=[('cd', 'CD'), ('vinyl', 'Vinyl')], max_length=5, null=True),
        ),
    ]