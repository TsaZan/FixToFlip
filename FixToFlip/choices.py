from django.db import models


class ProfileTypes(models.TextChoices):
    PERSONAL = 'Personal', 'Personal'
    COMPANY = 'Company', 'Company'


class PropertyTypeChoices(models.TextChoices):
    TOWNHOUSE = 'Townhouse', 'Townhouse'
    APARTMENT = 'Apartment', 'Apartment'
    CONDO = 'Condo', 'Condo'
    VILLA = 'Villa', 'Villa'


class ExpenseTypeChoices(models.TextChoices):
    bathrooms = 'bathroom_repair_expenses', 'Bathroom Repair Expenses'
    kitchen = 'kitchen_repair_expenses', 'Kitchen Repair Expenses'
    floors = 'floors_repair_expenses', 'Floors Repair Expenses'
    walls = 'walls_repair_expenses', 'Walls Repair Expenses'
    windows = 'windows_doors_repair_expenses', 'Windows and Doors Repair Expenses'
    plumbing = 'plumbing_repair_expenses', 'Plumbing Repair Expenses'
    electrical = 'electrical_repair_expenses', 'Electrical Repair Expenses'
    roof = 'roof_repair_expenses', 'Roof Repair Expenses'
    facade = 'facade_repair_expenses', 'Facade Repair Expenses'
    other = 'other_repair_expenses', 'Other Repair Expenses'
    utilities = 'utilities', 'Utilities'
    notary_taxes = 'notary_taxes', 'Notary Taxes'
    profit_Tax = 'profit_tax', 'Profit Tax'
    municipality_Taxes = 'municipality_taxes', 'Municipality Taxes'
    advertising = 'advertising', 'Advertising'
    administrative_Fees = 'administrative_fees', 'Administrative Fees'
    insurance = 'insurance', 'Insurance'
    other_expenses = 'other_expenses', 'Other Expenses'

    @classmethod
    def get_choice(cls, label):
        for choice in cls.choices:
            if choice[1] == label:
                return choice[0]
        raise ValueError(f"No field found for label: {label}")


class PropertySizeChoices(models.TextChoices):
    sqm = 'm', 'sqm'
    sqft = 'ft', 'sqft'


class CreditTypeChoices(models.TextChoices):
    CREDIT = 'Business Credit', 'Business Credit'
    DEBIT = 'Personal Credit', 'Personal Credit'
    MORTGAGE = 'Mortgage', 'Mortgage'


class OfferStatusChoices(models.TextChoices):
    ACTIVE = 'Active', 'Active'
    SOLD = 'Sold', 'Sold'


class PropertyConditionChoices(models.TextChoices):
    UNDER_REPAIR = 'Under repair', 'Under repair'
    REPAIRED = 'Repaired', 'Repaired'
    FOR_SALE = 'For sale', 'For sale'
    SOLD = 'Sold', 'Sold'


class PublishChoices(models.TextChoices):
    YES = 'True', 'Published'
    NO = 'False', 'Not Published'

