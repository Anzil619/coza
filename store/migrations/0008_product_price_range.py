# Generated by Django 4.2 on 2023-06-01 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_product_price_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_range',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.pricefilter'),
        ),
    ]
