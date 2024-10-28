from django.urls import path, include

from FixToFlip.properties.views import add_property, properties_main_page, edit_property, delete_property, \
    add_property_expenses, details_property, property_expenses_view

urlpatterns = [
    path('', properties_main_page, name='properties_main_page'),
    path('<int:pk>/', details_property, name='details_property'),
    path('<int:pk>/edit/', edit_property, name='edit_property'),
    path('<int:pk>/delete/', delete_property, name='delete_property'),
    path('<int:pk>/add-expenses/', add_property_expenses, name='add_property_expenses'),
    path('<int:pk>/convert/', property_expenses_view, name='property_expenses_view'),
]