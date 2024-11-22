from django.urls import path, include

from FixToFlip.properties.serializers import PropertyConditionChartData, PropertyExpenseData
from FixToFlip.properties.views import add_expense

urlpatterns = [
    path('', include([
        path('<int:pk>/expense/', add_expense, name='add_expense'),
        path('api-condition/', PropertyConditionChartData.as_view(), name='api_condition'),
        path('api-expenses/', PropertyExpenseData.as_view(), name='api_expenses'),
    ])),
]