# Generated by Django 5.1.1 on 2024-11-30 15:01

import FixToFlip.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_rename_company_location_country_profile_company_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseaccount',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.MinLengthValidator(2, 'First name must be at least 2 characters long.'), FixToFlip.validators.OnlyLettersValidator('First name must contain only letters')]),
        ),
        migrations.AlterField(
            model_name='baseaccount',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.MinLengthValidator(2, 'Last name must be at least 2 characters long.'), FixToFlip.validators.OnlyLettersValidator('Last name must contain only letters')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='company_name',
            field=models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.MinLengthValidator(2, 'Company name must be at least 2 characters long.')]),
        ),
    ]