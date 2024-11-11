from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal

from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from djmoney.money import Money

from FixToFlip.choices import CreditTypeChoices


class Credit(models.Model):
    class Meta:
        verbose_name = 'Credit'
        verbose_name_plural = 'Credits'
        ordering = ['-credit_term']

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
        return f'{self.credit_start_date} - {self.credit_amount}'


class CreditPayment(models.Model):
    class Meta:
        verbose_name = 'Credit Payment'
        verbose_name_plural = 'Credit Payments'
        ordering = ['-payment_date']

    payment_date = models.DateField()

    principal_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Money(0, 'EUR'),
        validators=[MinMoneyValidator(Decimal(0))]
    )

    interest_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Money(0, 'EUR'),
        validators=[MinMoneyValidator(Decimal(0))]
    )

    credit = models.ForeignKey(
        to=Credit,
        on_delete=models.DO_NOTHING,
        related_name='credit_payments',
    )

    def full_payment(self):
        return self.principal_amount + self.interest_amount


    def __str__(self):
        return f"{self.payment_date} - {self.full_payment()} - {self.credit.bank_name}"
