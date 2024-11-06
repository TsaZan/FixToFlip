from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from django.conf import settings

from FixToFlip.choices import PropertyTypeChoices, PropertyConditionChoices
from FixToFlip.credits.models import Credit
from FixToFlip.validators import get_current_date, get_current_year


class Property(models.Model):
    '''Property Basic Information. Can be added and seen by all types of authorized users.'''
    MAX_LENGTH = 100

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']

    property_name = models.CharField(
        max_length=MAX_LENGTH,
        null=True,
        blank=True,
    )

    property_description = models.TextField(
        null=True,
        blank=True,
    )

    country = models.CharField(
        max_length=MAX_LENGTH,
        null=True,
        blank=True,
    )

    city = models.CharField(
        max_length=MAX_LENGTH,
        null=True,
        blank=True,
    )

    address = models.CharField(
        max_length=MAX_LENGTH,
        null=True,
        blank=True,
    )

    property_type = models.CharField(
        max_length=MAX_LENGTH,
        choices=PropertyTypeChoices.choices,
        null=True,
        blank=True,

    )

    bedrooms = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    bathrooms = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    floor = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    year_of_built = models.SmallIntegerField(
    )

    property_size = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    bought_date = models.DateField(
        validators=[MaxValueValidator(get_current_date())],
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    property_condition = models.CharField(
        max_length=MAX_LENGTH,
        choices=PropertyConditionChoices.choices,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_properties',
    )

    def __str__(self):
        if self.property_name:
            return self.property_name
        return (f'Country: {self.country} , Location: {self.town} , '
                f'Address: {self.address}')


class PropertyForSale(Property):
    '''Properties listed for sales'''
    listed_price = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='EUR',
    )

    is_furnished = models.BooleanField(
        default=False,
    )

    list_description = models.TextField()

    listed_property = models.ForeignKey(
        to='Property',
        related_name='listed_for_sales',
        on_delete=models.SET_NULL,
        null=True,
    )

    listed_date = models.DateField(
        auto_now_add=True,
    )


class PropertyFinancialInformation(models.Model):
    '''Property financial information. Can be seen by property owners and another authorized users'''

    class Meta:
        verbose_name = 'Property Financial Information'
        verbose_name_plural = 'Property Financial Information'

    initial_price = MoneyField(max_digits=10, decimal_places=2, default=Money(0, 'EUR'))

    repair_cost = MoneyField(max_digits=10, decimal_places=2, default=Money(0, 'EUR'),
                             null=True,
                             blank=True,
                             )

    is_credited = models.BooleanField()

    credit = models.ForeignKey(
        to=Credit,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='credit_financial_information',
    )

    credited_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default=Money(0, 'EUR'),
    )

    property = models.ForeignKey(
        to='Property',
        on_delete=models.CASCADE,
        related_name='property_financial_information',
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.property)


class PropertyExpense(models.Model):
    '''Property expenses information. Can be seen by property owners and all authorized users.'''

    MAX_DIGITS = 7
    MAX_DECIMAL_PLACES = 2

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'

    utilities = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        null=True,
        blank=True,
    )

    notary_taxes = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        null=True,
        blank=True,
    )

    profit_tax = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        null=True,
        blank=True,
    )

    municipality_taxes = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        null=True,
        blank=True,
    )

    advertising = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        null=True,
        blank=True,
    )

    administrative_fees = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        null=True,
        blank=True,
    )

    insurance = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        null=True,
        blank=True,
    )

    expected_expenses = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        null=True,
        blank=True,
    )
    property = models.ForeignKey(
        to='Property',
        on_delete=models.CASCADE,
        related_name='property_expenses',
        blank=False,
        null=False,
    )

    expense_details = models.TextField(blank=True, null=True)

    expense_date = models.DateField(blank=True, null=True)
