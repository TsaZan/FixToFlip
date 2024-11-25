from django.urls import path, include

from FixToFlip.properties.views import add_expense, PropertyConditionChartData, PropertyExpenseData, \
    DashboardPropertiesView, property_add_view, PropertyDetailsView, PropertyEditView, PropertyDeleteView, \
    DashboardExpensesView, delete_expense

urlpatterns = [
    path('', include([
        path('', include([
            path('', DashboardPropertiesView.as_view(), name='dashboard_properties'),
            path('add-property/', property_add_view, name='add_property'),
            path('<int:pk>/view/', PropertyDetailsView.as_view(), name='property_details'),
            path('<int:pk>/edit/', PropertyEditView.as_view(), name='edit_property'),
            path('<int:pk>/delete/', PropertyDeleteView.as_view(), name='delete_property'),
        ])),
        path('expenses/', DashboardExpensesView.as_view(), name='dashboard_expenses'),

        path('<int:pk>/expense/', add_expense, name='add_expense'),
        path('expense/<int:pk>/delete/', delete_expense, name='delete_expense'),

        path('api-condition/', PropertyConditionChartData.as_view(), name='api_condition'),
        path('api-expenses/', PropertyExpenseData.as_view(), name='api_expenses'),
    ])),
]