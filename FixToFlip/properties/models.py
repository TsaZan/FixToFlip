from decimal import Decimal

from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from djmoney.money import Money
from django.conf import settings

from FixToFlip.choices import PropertyTypeChoices, PropertyConditionChoices
from FixToFlip.credits.models import Credit


class Property(models.Model):
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
        null=True,
        blank=True,
    )

    property_size = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    bought_date = models.DateField(
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
        return (f'Country: {self.country} , Location: {self.city} , '
                f'Address: {self.address}')


class PropertyFinancialInformation(models.Model):
    class Meta:
        verbose_name = 'Property Financial Information'
        verbose_name_plural = 'Property Financial Information'

    initial_price = MoneyField(max_digits=10,
                               decimal_places=2,
                               default=Money(0, 'EUR'),
                               validators=[MinMoneyValidator(
                                   Decimal(0),
                                   message='Initial property price cannot be negative.'
                               )],
                               )

    repair_cost = MoneyField(max_digits=10, decimal_places=2,
                             default=Money(0, 'EUR'),
                             validators=[MinMoneyValidator(
                                 Decimal(0),
                                 message='Repair cost cannot be negative.'
                             )],
                             null=True,
                             blank=True,
                             )

    is_credited = models.BooleanField(
        default=False,
        null=False,
    )

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
        validators=[MinMoneyValidator(
            Decimal(0),
            message='Credited amount cannot be negative.'
        )],
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

    MAX_DIGITS = 10
    MAX_DECIMAL_PLACES = 2

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ['-last_expense_date']

    utilities = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Utilities',
        null=True,
        blank=True,
    )

    notary_taxes = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Notary Taxes',
        null=True,
        blank=True,
    )

    profit_tax = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Profit Tax',
        null=True,
        blank=True,
    )

    municipality_taxes = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Municipality Taxes',

        null=True,
        blank=True,
    )

    advertising = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Advertising',
        null=True,
        blank=True,
    )

    administrative_fees = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Administrative Fees',
        null=True,
        blank=True,
    )

    insurance = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Insurance',
        null=True,
        blank=True,
    )

    credit_interest = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Credit Interest',
        null=True,
        blank=True,
    )

    other_expenses = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Other Expenses',
        null=True,
        blank=True,
    )

    expected_expenses = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        validators=[MinMoneyValidator(Decimal(0), message='Expected expenses cannot be negative.')],
        verbose_name='Expected Expenses',
        null=True,
        blank=True,
    )

    bathroom_repair_expenses = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Bathroom Repair Expenses',
        null=True,
        blank=True,
    )

    kitchen_repair_expenses = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Kitchen Repair Expenses',
        null=True,
        blank=True,
    )

    floors_repair_expenses = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Floors Repair Expenses',
        null=True,
        blank=True,
    )

    walls_repair_expenses = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Walls Repair Expenses',
        null=True,
        blank=True,
    )

    windows_doors_repair_expenses = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Windows and Doors Repair Expenses',
        null=True,
        blank=True,
    )

    plumbing_repair_expenses = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Plumbing Repair Expenses',
        null=True,
        blank=True,
    )

    electrical_repair_expenses = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Electrical Repair Expenses',
        null=True,
        blank=True,
    )

    roof_repair_expenses = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Insurance',
        null=True,
        blank=True,
    )

    facade_repair_expenses = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Facade Repair Expenses',
        null=True,
        blank=True,
    )

    other_repair_expenses = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        verbose_name='Other Repair Expenses',
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

    last_expense_date = models.DateField(
        blank=True,
        null=True,
        auto_now=True)

    def expense_total(self):
        return (self.utilities + self.notary_taxes + self.profit_tax + self.municipality_taxes +
                self.advertising + self.administrative_fees + self.insurance + self.other_expenses + self.credit_interest)

    def total_repair_expenses(self):
        return (self.plumbing_repair_expenses + self.electrical_repair_expenses + self.windows_doors_repair_expenses
                + self.roof_repair_expenses + self.facade_repair_expenses + self.walls_repair_expenses
                + self.floors_repair_expenses + self.kitchen_repair_expenses +
                self.bathroom_repair_expenses + self.other_repair_expenses)

    def actual_expenses(self):
        return self.expense_total() + self.total_repair_expenses()

    def remaining_expected_expenses(self):
        return self.expected_expenses - self.expense_total()

    def expenses_per_sqm(self):
        if self.property.property_size == 0 or self.property.property_size is None:
            return 0
        elif self.actual_expenses() == 0 or self.actual_expenses() is None:
            return 0
        return self.actual_expenses() / self.property.property_size

    def biggest_expense(self):
        expenses = {
            'utilities': self.utilities,
            'notary_taxes': self.notary_taxes,
            'profit_tax': self.profit_tax,
            'municipality_taxes': self.municipality_taxes,
            'advertising': self.advertising,
            'administrative_fees': self.administrative_fees,
            'insurance': self.insurance,
            'other_expenses': self.other_repair_expenses,

        }
        biggest_expense_name = max(expenses, key=expenses.get)

        verbose_name = self._meta.get_field(biggest_expense_name).verbose_name

        return verbose_name, expenses[biggest_expense_name]

    def __str__(self):
        return (f'Property: {str(self.property)} - Added Expenses: {self.expense_total()} '
                f'- Expected Expenses: {self.expected_expenses}')


class PropertyExpenseNotes(models.Model):
    notes = models.TextField(
        blank=True,
        null=True,
    )

    expense_amount = MoneyField(
        max_digits=PropertyExpense.MAX_DIGITS,
        decimal_places=PropertyExpense.MAX_DECIMAL_PLACES,
        validators=[MinMoneyValidator(
            Decimal(0),
            message='Expense amount cannot be negative.'
        )],

    )

    expense_type = models.CharField()

    expense_date = models.DateField(
        blank=True,
        null=True

    )
    relates_expenses = models.ForeignKey(
        to='PropertyExpense',
        related_name='expenses_notes',
        on_delete=models.CASCADE
    )
