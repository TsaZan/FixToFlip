from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal

from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from djmoney.money import Money

from FixToFlip.choices import CreditTypeChoices


class Credit(models.Model):
    bank_name = models.CharField(
        max_length=100
    )

    credit_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Money(0, 'EUR'),
        validators=[MinMoneyValidator(Decimal(0))]
    )

    amounts_paid = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Money(0, 'EUR'),
        validators=[MinMoneyValidator(Decimal(0))],
        null=True,
        blank=True
    )

    credit_interest = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    monthly_payment = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Money(0, 'EUR'),
        validators=[MinMoneyValidator(Decimal(0))]
    )
    credit_description = models.TextField(
        blank=True,
        null=True,
        help_text='You can add all usefull information about your credit e.g. '
                  'credit consultant name, phone number, etc.')

    credit_start_date = models.DateField()

    credit_term = models.DateField()

    credit_type = models.CharField(
        max_length=30,
        choices=CreditTypeChoices.choices,
    )

    credit_owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.bank_name
