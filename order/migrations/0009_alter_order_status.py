# Generated by Django 4.2 on 2023-05-23 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Out For Shipping', 'Out For Shipping')], default='Pending', max_length=150),
        ),
    ]
