# Generated by Django 5.1.1 on 2024-11-28 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0017_alter_propertyexpense_expected_expenses"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PropertyForSale",
        ),
    ]
