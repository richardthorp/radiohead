# Generated by Django 3.2.4 on 2021-08-04 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_alter_orderlineitem_format'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address_line2',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='orderlineitem',
            name='size',
            field=models.CharField(blank=True, choices=[('s', 'S'), ('m', 'M'), ('l', 'L')], max_length=1, null=True),
        ),
    ]