# Generated by Django 4.2 on 2023-06-01 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_product_price_range'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_range',
        ),
    ]
