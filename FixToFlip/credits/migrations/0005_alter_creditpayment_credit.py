# Generated by Django 5.1.1 on 2024-11-11 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("credits", "0004_creditpayment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="creditpayment",
            name="credit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="credit_payments",
                to="credits.credit",
            ),
        ),
    ]
