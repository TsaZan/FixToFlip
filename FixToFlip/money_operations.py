from django.db.models import Sum
from djmoney.money import Money

from FixToFlip.credits.models import Credit, CreditPayment
from FixToFlip.properties.models import PropertyExpense


def sum_current_expenses(property_id):
    expenses = PropertyExpense.objects.filter(property_id=property_id).values(
        'utilities', 'notary_taxes', 'profit_tax', 'municipality_taxes',
        'advertising', 'administrative_fees', 'insurance', 'other_expenses',
        'bathroom_repair_expenses', 'kitchen_repair_expenses', 'plumbing_repair_expenses',
        'electrical_repair_expenses', 'floors_repair_expenses', 'walls_repair_expenses',
        'roof_repair_expenses', 'facade_repair_expenses', 'windows_doors_repair_expenses'
    ).first()

    if not expenses:
        return 0

    return sum(expenses[field] for field in expenses if expenses[field] is not None)


def credit_reminder_calculation(credit_id):
    credit = Credit.objects.filter(id=credit_id)
    remainder = credit[0].credit_amount - credit[0].amounts_paid
    return remainder


def credit_balance(credit_id):
    credit = Credit.objects.get(id=credit_id)
    total_principal_amount = CreditPayment.objects.filter(credit_id=credit_id).aggregate(Sum('principal_amount'))[
        'principal_amount__sum']
    if total_principal_amount is None:
        total_principal_amount = Money(0, credit.credit_amount.currency)

    if not isinstance(total_principal_amount, Money):
        total_principal_amount = Money(total_principal_amount, credit.credit_amount.currency)

    balance = credit.credit_amount - total_principal_amount
    return balance


def interest_paid(credit_id):
    credit = Credit.objects.get(id=credit_id)
    total_principal_amount = CreditPayment.objects.filter(credit_id=credit_id).aggregate(Sum('interest_amount'))[
        'interest_amount__sum']

    if total_principal_amount is None:
        total_interest_amount = Money(0, credit.credit_amount.currency)

    if not isinstance(total_principal_amount, Money):
        total_interest_amount = Money(total_principal_amount, credit.credit_amount.currency)
    return total_interest_amount
