# Generated by Django 4.2 on 2023-06-13 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0023_usercoupon_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercoupon',
            name='order',
        ),
    ]
