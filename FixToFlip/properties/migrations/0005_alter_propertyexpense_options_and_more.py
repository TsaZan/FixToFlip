# Generated by Django 5.1.1 on 2024-11-06 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_alter_property_country'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='propertyexpense',
            options={'ordering': ['-last_expense_date'], 'verbose_name': 'Expense', 'verbose_name_plural': 'Expenses'},
        ),
        migrations.RemoveField(
            model_name='propertyexpense',
            name='expense_date',
        ),
        migrations.AddField(
            model_name='propertyexpense',
            name='last_expense_date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]