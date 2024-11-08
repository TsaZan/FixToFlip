from django.db import models


class UserRoles(models.TextChoices):
    INVESTOR = 'i', 'Investor'
    BROKER = 'b', 'Broker'


class CurrencyChoices(models.TextChoices):
    BGN = 'BGN', 'BGN'
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'
    GBP = 'GBP', 'GBP'
    AED = 'AED', 'AED'
    CHF = 'CHF', 'CHF'


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
