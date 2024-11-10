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
