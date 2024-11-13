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
    utilities = 'utilities', 'Utilities'
    notary_taxes = 'notary_taxes', 'Notary Taxes'
    Profit_Tax = 'profit_tax', 'Profit Tax'
    Municipality_Taxes = 'municipality_taxes', 'Municipality Taxes'
    Advertising = 'advertising', 'Advertising'
    Administrative_Fees = 'administrative_fees', 'Administrative Fees'
    Insurance = 'insurance', 'Insurance'


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
