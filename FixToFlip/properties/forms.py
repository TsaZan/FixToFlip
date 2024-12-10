from django import forms
from djmoney.forms import MoneyField

from FixToFlip.choices import ExpenseTypeChoices
from FixToFlip.credits.models import Credit
from FixToFlip.properties.models import (
    Property,
    PropertyExpense,
    PropertyFinancialInformation,
    PropertyExpenseNotes,
)


class PropertyBaseForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ["owner"]
        widgets = {
            "bought_date": forms.DateInput(
                attrs={"type": "date", "min": "1900-01-01", "placeholder": "YYYY-MM-DD"}
            ),
            "property_name": forms.TextInput(attrs={"placeholder": "Property Name"}),
            "property_description": forms.Textarea(
                attrs={
                    "placeholder": "Property Description",
                    "class": "form-control",
                    "rows": 6,
                }
            ),
            "country": forms.TextInput(attrs={"placeholder": "Country"}),
            "city": forms.TextInput(attrs={"placeholder": "City"}),
            "address": forms.TextInput(attrs={"placeholder": "Address"}),
            "property_size": forms.NumberInput(
                attrs={"placeholder": "Property Size (sqm)"}
            ),
            "bedrooms": forms.NumberInput(attrs={"placeholder": "Number of Bedrooms"}),
            "bathrooms": forms.NumberInput(
                attrs={"placeholder": "Number of Bathrooms"}
            ),
            "year_of_built": forms.NumberInput(
                attrs={"placeholder": "Construction Year"}
            ),
            "floor": forms.NumberInput(attrs={"placeholder": "Floor Number"}),
            "notes": forms.Textarea(attrs={"placeholder": "Additional Notes"}),
        }

        labels = {
            "property_name": "Property Name",
            "property_type": "Property Type",
            "property_size": "Property Size",
            "bought_date": "Bought Date",
        }


class PropertyAddForm(PropertyBaseForm):
    pass


class PropertyFinanceInformationForm(forms.ModelForm):
    class Meta:
        model = PropertyFinancialInformation
        fields = "__all__"


class PropertyEditForm(PropertyBaseForm):
    pass


class PropertyDeleteForm(PropertyBaseForm):
    class Meta:
        model = Property
        fields = []


class PropertyExpenseForm(forms.ModelForm):
    class Meta:
        inline_classes = ["inline-formset"]

        model = PropertyExpense
        fields = "__all__"
        exclude = ["property", "expense_currency"]


class AddExpenseForm(forms.Form):
    expense_types = forms.ChoiceField(
        choices=ExpenseTypeChoices, label="Choose Expense Type"
    )
    amount = MoneyField(max_digits=14, decimal_places=2, label="Amount")


class ExpenseNotesForm(forms.ModelForm):
    class Meta:
        model = PropertyExpenseNotes
        fields = ("notes", "expense_date")
        widgets = {
            "expense_date": forms.DateInput(
                attrs={"type": "date", "min": "1900-01-01", "placeholder": "YYYY-MM-DD"}
            ),
        }


class AddCreditToPropertyForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["credit"].choices = [
                (credit.id, str(credit))
                for credit in Credit.objects.filter(credit_owner=user)
            ]

    credited_amount = MoneyField(
        max_digits=14,
        decimal_places=2,
        label="Credit Amount",
    )
    credit = forms.ChoiceField(choices=[], label="Select a Credit")
