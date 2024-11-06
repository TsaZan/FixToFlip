from FixToFlip.properties.models import Property, PropertyExpense


@staticmethod
def sum_current_expenses(property):
    property = Property.objects.get(pk=property)
    expenses = PropertyExpense.objects.filter(property_id__exact=property.id)

    utilities = expenses.values_list('utilities', flat=True)
    notary_taxes = expenses.values_list('notary_taxes', flat=True)
    profit_tax= expenses.values_list('profit_tax', flat=True)
    municipality_taxes= expenses.values_list('municipality_taxes', flat=True)
    advertising= expenses.values_list('advertising', flat=True)
    administrative_fees= expenses.values_list('administrative_fees', flat=True)
    insurance = expenses.values_list('insurance', flat=True)

    return sum([utilities[0], notary_taxes[0], profit_tax[0], municipality_taxes[0], advertising[0], administrative_fees[0], insurance[0]])