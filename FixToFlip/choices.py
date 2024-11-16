from django.db import models


class ProfileTypes(models.TextChoices):
    PERSONAL = 'Personal', 'Personal'
    COMPANY = 'Company', 'Company'


class PropertyTypeChoices(models.TextChoices):
    TOWNHOUSE = 'TH', 'Townhouse'
    APARTMENT = 'AP', 'Apartment'
    CONDO = 'C', 'Condo'
    VILLA = 'V', 'Villa'
    CARAVAN = 'CN', 'Caravan'


class ExpenseTypeChoices(models.TextChoices):
    bathrooms = 'bathroom_repair_expenses', 'Bathroom Repair Expenses'
    kitchen = 'kitchen_repair_expenses', 'Kitchen Repair Expenses'
    plumbing = 'plumbing_repair_expenses', 'Plumbing Repair Expenses'
    electrical = 'electrical_repair_expenses', 'Electrical Repair Expenses'
    floors = 'floors_repair_expenses', 'Floors Repair Expenses'
    walls = 'walls_repair_expenses', 'Walls Repair Expenses'
    roof = 'roof_repair_expenses', 'Roof Repair expenses'
    facade = 'facade_repair_expenses', 'Facade Repair Expenses'
    windows = 'windows_doors_repair_expenses', 'Windows and Doors Repair Expenses'
    other = 'other_repair_expenses', 'Other Repair Expenses'
    utilities = 'utilities', 'Utilities'
    notary_taxes = 'notary_taxes', 'Notary Taxes'
    profit_Tax = 'profit_tax', 'Profit Tax'
    municipality_Taxes = 'municipality_taxes', 'Municipality Taxes'
    advertising = 'advertising', 'Advertising'
    administrative_Fees = 'administrative_fees', 'Administrative Fees'
    insurance = 'insurance', 'Insurance'
    other_oxpenses = 'other_expenses', 'Other Expenses'



class PropertySizeChoices(models.TextChoices):
    sqm = 'm', 'sqm'
    sqft = 'ft', 'sqft'


class CreditTypeChoices(models.TextChoices):
    CREDIT = 'B', 'Business Credit'
    DEBIT = 'P', 'Personal Credit'
    MORTGAGE = 'M', 'Mortgage'


class OfferStatusChoices(models.TextChoices):
    PROPOSED = 'P', 'Proposed'
    ACTIVE = 'A', 'Active'
    NEGOTIATIONS = 'N', 'Negotiations'
    EXPIRED = 'E', 'Expired'
    SOLD = 'S', 'Sold'


class PropertyConditionChoices(models.TextChoices):
    READY = 'Ready to sell', 'Ready to sell'
    SOLD = 'Sold', 'Sold'
    FOR_SALE = 'For sale', 'For sale'
    REPAIRED = 'Repaired', 'Repaired'
    UNDER_REPAIR = 'Under repair', 'Under repair'
