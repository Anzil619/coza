# Generated by Django 4.2 on 2023-06-13 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0022_remove_order_status_orderitem_status_returnorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercoupon',
            name='total_price',
            field=models.FloatField(null=True),
        ),
    ]
