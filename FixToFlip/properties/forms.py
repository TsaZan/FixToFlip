from cities_light.admin import Country
from django import forms
from django.views.generic import DeleteView
from djmoney.forms import MoneyField

from FixToFlip.choices import ExpenseTypeChoices
from FixToFlip.credits.models import Credit
from FixToFlip.properties.models import Property, PropertyForSale, PropertyExpense, PropertyFinancialInformation
from FixToFlip.validators import get_current_date


class PropertyBaseForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['owner']
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


class PropertyEditForm(PropertyBaseForm):
    pass


class PropertyDeleteForm(PropertyBaseForm):
    class Meta:
        model = Property
        fields = []


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


# class PropertyFinancialInformationForm(forms.ModelForm):
#     class Meta:
#         model = PropertyFinancialInformation
#         fields = '__all__'


class PropertyExpenseForm(forms.ModelForm):
    class Meta:
        inline_classes = ['inline-formset']

        model = PropertyExpense
        fields = '__all__'
        exclude = ['property', 'expense_currency']


class AddExpenseForm(forms.Form):
    expense_types = forms.ChoiceField(choices=ExpenseTypeChoices, label='Choose Expense Type')
    amount = MoneyField(max_digits=14, decimal_places=2, label='Amount')


class AddCreditToPropertyForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['credit'].choices = [
                (credit.id, str(credit))
                for credit in Credit.objects.filter(credit_owner=user)]

    credited_amount = MoneyField(
        max_digits=14,
        decimal_places=2,
        label='Credit Amount',
    )
    credit = forms.ChoiceField(
        choices=[],
        label='Select a Credit'
    )
