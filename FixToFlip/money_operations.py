from FixToFlip.credits.models import Credit
from FixToFlip.properties.models import Property, PropertyExpense


def sum_current_expenses(property_id):
    expenses = PropertyExpense.objects.filter(property_id=property_id).values(
        'utilities', 'notary_taxes', 'profit_tax', 'municipality_taxes',
        'advertising', 'administrative_fees', 'insurance'
    ).first()

    if not expenses:
        return 0

    return sum(expenses[field] for field in expenses if expenses[field] is not None)


def credit_reminder_calculation(credit_id):
    credit = Credit.objects.filter(id=credit_id)
    remainder = credit[0].credit_amount - credit[0].amounts_paid
    return remainder


