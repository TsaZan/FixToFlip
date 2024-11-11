from django import forms

from FixToFlip.credits.models import Credit, CreditPayment


class CreditBaseForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = '__all__'


class CreditAddForm(CreditBaseForm):
    class Meta:
        model = Credit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['credit_owner'].required = False


class CreditEditForm(CreditBaseForm):
    pass


class CreditDeleteForm(CreditBaseForm):
    pass


class CreditPaymentForm(forms.ModelForm):
    class Meta:
        model = CreditPayment
        fields = ['payment_date', 'principal_amount', 'interest_amount', 'credit']  # Include relevant fields
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'principal_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'interest_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'credit': forms.HiddenInput(),
        }
