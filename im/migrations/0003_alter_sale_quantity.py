# Generated by Django 5.1.3 on 2024-11-25 15:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("im", "0002_product_order_pack"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sale",
            name="quantity",
            field=models.IntegerField(help_text="Quantity of the product sold"),
        ),
    ]
