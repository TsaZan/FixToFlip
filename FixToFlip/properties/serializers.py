from rest_framework import serializers

from FixToFlip.properties.models import Property, PropertyForSale, PropertyFinancialInformation, PropertyExpense


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['property_name', 'country', 'city', 'address',
                  'property_type', 'property_size', 'bought_date', 'property_condition']


class PropertiesForSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyForSale
        fields = ['__all__']


class PropertyFinancialInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFinancialInformation
        fields = ['__all__']


class PropertyExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyExpense
        exclude = ['property',]
