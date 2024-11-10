import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0005_alter_propertyexpense_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='bought_date',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2024, 11, 9))]),
        ),
    ]
