from cities_light.admin import Country
from django import forms

from FixToFlip.properties.models import Property, PropertyForSale, PropertyExpense, PropertyFinancialInformation
from FixToFlip.validators import get_current_date


class PropertyBaseForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        widgets = {
            'bought_date': forms.DateInput(attrs={
                'type': 'date',
                'max': get_current_date(),
                'min': '1900-01-01'}),
            'property_name': forms.TextInput(attrs={'placeholder': 'Property Name'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'town': forms.TextInput(attrs={'placeholder': 'Town'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address'}),
            'post_code': forms.TextInput(attrs={'placeholder': 'Post Code'}),
        }

        labels = {
            'property_name': 'Property Name',
            'property_type': 'Property Type',
            'property_size': 'Property Size',
            'bought_date': 'Bought Date',
        }


class PropertyAddForm(PropertyBaseForm):
    class Meta:
        model = Property
        exclude = ['owner']


class PropertyFinanceInformationForm(forms.ModelForm):
    class Meta:
        model = PropertyFinancialInformation
        fields = '__all__'
        widgets = {
            'initial_price': forms.TextInput(attrs={'placeholder': 'Initial Price', }),
            'credited_amount': forms.TextInput(attrs={'placeholder': 'Credited Amount', 'type': 'input', }),
        }


class PropertyEditForm(PropertyBaseForm):
    pass


class PropertyDeleteForm(forms.ModelForm):
    pass


class PropertyForSaleForm(forms.ModelForm):
    class Meta:
        model = PropertyForSale
        fields = '__all__'
        widgets = {
            'listed_price': forms.TextInput(attrs={'placeholder': 'Price'}),
            'list_description': forms.Textarea(attrs={'placeholder': 'Description'}),
        }

        labels = {
            'listed_price': '',
            'list_description': '',

        }


class PropertyFinancialInformationForm(forms.ModelForm):
    class Meta:
        model = PropertyFinancialInformation
        fields = '__all__'


class PropertyExpenseForm(forms.ModelForm):
    class Meta:
        inline_classes = ['inline-formset']

        model = PropertyExpense
        fields = '__all__'
        exclude = ['property', 'expense_currency']
