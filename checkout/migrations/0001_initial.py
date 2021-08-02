# Generated by Django 3.2.4 on 2021-08-02 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0007_alter_album_year'),
        ('profiles', '0005_auto_20210705_0944'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(editable=False, max_length=32)),
                ('email', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=60)),
                ('phone_number', models.CharField(max_length=30)),
                ('address_line1', models.CharField(max_length=80)),
                ('address_line2', models.CharField(max_length=80)),
                ('town_or_city', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=80)),
                ('country', models.CharField(max_length=80)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('delivery_cost', models.DecimalField(decimal_places=2, max_digits=4)),
                ('order_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('grand_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='profiles.profile')),
            ],
        ),
        migrations.CreateModel(
            name='OrderLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=1)),
                ('format', models.CharField(blank=True, max_length=5, null=True)),
                ('quantity', models.IntegerField()),
                ('lineitem_total', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.album')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineiems', to='checkout.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.product')),
            ],
        ),
    ]
