from django.db.models import Sum
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from FixToFlip.choices import PropertyConditionChoices, ExpenseTypeChoices
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
        exclude = ['property', ]


class PropertyConditionChartData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        conditions = [choice[0] for choice in PropertyConditionChoices.choices]
        if not user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=403)

        data = {
            condition: Property.objects.filter(owner=user, property_condition=condition).count()
            for condition in conditions
        }
        return Response(data)


class PropertyExpenseData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=403)

        expenses_data = {
            'utilities': PropertyExpense.objects.filter(property__owner=user)
                         .aggregate(Sum('utilities'))['utilities__sum'] or 0,
            'notary_taxes': PropertyExpense.objects.filter(property__owner=user)
                            .aggregate(Sum('notary_taxes'))['notary_taxes__sum'] or 0,
            'profit_tax': PropertyExpense.objects.filter(property__owner=user)
                          .aggregate(Sum('profit_tax'))['profit_tax__sum'] or 0,
            'municipality_taxes': PropertyExpense.objects.filter(property__owner=user)
                                  .aggregate(Sum('municipality_taxes'))['municipality_taxes__sum'] or 0,
            'advertising': PropertyExpense.objects.filter(property__owner=user)
                           .aggregate(Sum('advertising'))['advertising__sum'] or 0,
            'administrative_fees': PropertyExpense.objects.filter(property__owner=user)
                                   .aggregate(Sum('administrative_fees'))['administrative_fees__sum'] or 0,
            'insurance': PropertyExpense.objects.filter(property__owner=user)
                         .aggregate(Sum('insurance'))['insurance__sum'] or 0,
            'other_expenses': PropertyExpense.objects.filter(property__owner=user)
                              .aggregate(Sum('other_expenses'))['other_expenses__sum'] or 0,
            'bathroom_repair_expenses': PropertyExpense.objects.filter(property__owner=user)
                                        .aggregate(Sum('bathroom_repair_expenses'))[
                                            'bathroom_repair_expenses__sum'] or 0,
            'kitchen_repair_expenses': PropertyExpense.objects.filter(property__owner=user)
                                       .aggregate(Sum('kitchen_repair_expenses'))['kitchen_repair_expenses__sum'] or 0,
            'floors_repair_expenses': PropertyExpense.objects.filter(property__owner=user)
                                      .aggregate(Sum('floors_repair_expenses'))['floors_repair_expenses__sum'] or 0,
            'walls_repair_expenses': PropertyExpense.objects.filter(property__owner=user)
                                     .aggregate(Sum('walls_repair_expenses'))['walls_repair_expenses__sum'] or 0,
            'windows_doors_repair_expenses': PropertyExpense.objects.filter(property__owner=user)
                                             .aggregate(Sum('windows_doors_repair_expenses'))[
                                                 'windows_doors_repair_expenses__sum'] or 0,
            'plumbing_repair_expenses': PropertyExpense.objects.filter(property__owner=user)
                                        .aggregate(Sum('plumbing_repair_expenses'))[
                                            'plumbing_repair_expenses__sum'] or 0,
            'electrical_repair_expenses': PropertyExpense.objects.filter(property__owner=user)
                                          .aggregate(Sum('electrical_repair_expenses'))[
                                              'electrical_repair_expenses__sum'] or 0,
            'roof_repair_expenses': PropertyExpense.objects.filter(property__owner=user)
                                    .aggregate(Sum('roof_repair_expenses'))['roof_repair_expenses__sum'] or 0,
            'facade_repair_expenses': PropertyExpense.objects.filter(property__owner=user)
                                      .aggregate(Sum('facade_repair_expenses'))['facade_repair_expenses__sum'] or 0,
            'other_repair_expenses': PropertyExpense.objects.filter(property__owner=user)
                                     .aggregate(Sum('other_repair_expenses'))['other_repair_expenses__sum'] or 0
        }
        return Response(expenses_data)
