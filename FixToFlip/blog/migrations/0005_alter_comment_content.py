# Generated by Django 5.1.1 on 2024-12-11 11:52

import FixToFlip.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_alter_comment_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="content",
            field=models.TextField(
                validators=[
                    django.core.validators.MinLengthValidator(
                        10, "Comment must be at least 10 characters long"
                    ),
                    FixToFlip.validators.bad_words_validator,
                ]
            ),
        ),
    ]
