# Generated by Django 5.1.3 on 2024-12-14 11:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("im", "0015_region_sale_region"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventory",
            name="date",
            field=models.DateField(
                db_index=True, help_text="Date of the inventory record"
            ),
        ),
    ]