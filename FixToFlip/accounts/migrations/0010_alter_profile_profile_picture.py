# Generated by Django 5.1.1 on 2024-12-11 11:52

import FixToFlip.validators
import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_baseaccount_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, validators=[FixToFlip.validators.image_validator], verbose_name='image'),
        ),
    ]