from django import forms
from djmoney.forms import MoneyField

from FixToFlip.choices import ExpenseTypeChoices
from FixToFlip.credits.models import Credit
from FixToFlip.properties.models import Property, PropertyForSale, PropertyExpense, PropertyFinancialInformation, \
    PropertyExpenseNotes


class PropertyBaseForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['owner']
        widgets = {
            'bought_date': forms.DateInput(attrs={
                'type': 'date', 'min': '1900-01-01', 'placeholder': 'YYYY-MM-DD'}),
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
    pass


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


class PropertyExpenseForm(forms.ModelForm):
    class Meta:
        inline_classes = ['inline-formset']

        model = PropertyExpense
        fields = '__all__'
        exclude = ['property', 'expense_currency']


class AddExpenseForm(forms.Form):
    expense_types = forms.ChoiceField(choices=ExpenseTypeChoices, label='Choose Expense Type')
    amount = MoneyField(max_digits=14, decimal_places=2, label='Amount')


class ExpenseNotesForm(forms.ModelForm):
    class Meta:
        model = PropertyExpenseNotes
        fields = ('notes', 'expense_date')


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
