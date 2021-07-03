# Generated by Django 3.2.4 on 2021-07-03 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=80),
        ),
    ]
