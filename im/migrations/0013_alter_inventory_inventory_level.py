# Generated by Django 5.1.3 on 2024-12-04 18:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("im", "0012_product_category_product_manufacturer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventory",
            name="inventory_level",
            field=models.FloatField(
                help_text="Current stock level of the product in the store"
            ),
        ),
    ]