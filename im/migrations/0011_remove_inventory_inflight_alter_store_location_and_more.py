# Generated by Django 5.1.3 on 2024-11-27 15:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("im", "0010_inventory_inflight"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="inventory",
            name="inflight",
        ),
        migrations.AlterField(
            model_name="store",
            name="location",
            field=models.CharField(
                blank=True, help_text="Store location", max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="store",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]