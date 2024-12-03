from rest_framework import serializers
from FixToFlip.properties.models import Property, PropertyFinancialInformation, PropertyExpense, PropertyExpenseNotes


class PropertyFinancialInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFinancialInformation
        fields = ['initial_price', 'repair_cost']


class PropertyExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyExpense
        fields = [
            'id',
            'utilities',
            'notary_taxes',
            'profit_tax',
            'municipality_taxes',
            'advertising',
            'administrative_fees',
            'insurance',
            'other_expenses',
            'bathroom_repair_expenses',
            'kitchen_repair_expenses',
            'floors_repair_expenses',
            'walls_repair_expenses',
            'windows_doors_repair_expenses',
            'plumbing_repair_expenses',
            'electrical_repair_expenses',
            'roof_repair_expenses',
            'facade_repair_expenses',
            'other_repair_expenses',
        ]


def finance_property_data(property_instance, financial_data, expenses_data):
    for finance in financial_data:
        PropertyFinancialInformation.objects.create(property=property_instance, **finance)
    for expense in expenses_data:
        PropertyExpense.objects.create(property=property_instance, **expense)


class BulkPropertySerializer(serializers.ListSerializer):
    def create(self, validated_data):
        user = self.context['request'].user
        created_properties = []

        for property_data in validated_data:
            financial_data = property_data.pop('property_financial_information', [])
            expenses_data = property_data.pop('property_expenses', [])
            property_data['owner'] = user

            new_property = Property.objects.create(**property_data)
            finance_property_data(new_property, financial_data, expenses_data)

            created_properties.append(new_property)

        return created_properties


class PropertySerializer(serializers.ModelSerializer):
    property_financial_information = PropertyFinancialInformationSerializer(many=True)
    property_expenses = PropertyExpenseSerializer(many=True)

    class Meta:
        model = Property
        fields = ['pk', 'property_name', 'country', 'city', 'address',
                  'property_type', 'property_size', 'bought_date', 'property_condition', 'property_description',
                  'bedrooms', 'bathrooms', 'floor', 'year_of_built', 'notes', 'property_financial_information',
                  'property_expenses']
        list_serializer_class = BulkPropertySerializer

    def create(self, validated_data):
        property_financial_data = validated_data.pop('property_financial_information', [])
        property_expenses_data = validated_data.pop('property_expenses', [])

        validated_data['owner'] = self.context['request'].user
        new_property = Property.objects.create(**validated_data)
        finance_property_data(new_property, property_financial_data, property_expenses_data)

        return new_property


class ExpenseNotesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyExpenseNotes
        fields = ['id', 'notes', 'expense_amount', 'expense_type', 'expense_date']

    def create(self, validated_data):
        relates_expenses = self.context.get('relates_expenses')

        expense_note = PropertyExpenseNotes.objects.create(
            relates_expenses=relates_expenses,
            **validated_data
        )

        expense_type = validated_data.get('expense_type')
        expense_amount = validated_data.get('expense_amount')

        if hasattr(relates_expenses, expense_type):
            current_value = getattr(relates_expenses, expense_type, 0)
            setattr(relates_expenses, expense_type, current_value + expense_amount)
            relates_expenses.save()
        else:
            raise serializers.ValidationError(
                {"expense_type": f"Invalid expense type: {expense_type}"}
            )

        return expense_note

