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
        self.fields['credit_type'].widget.attrs['class'] = 'btn btn-two btn-lg dropdown-toggle'
        self.fields['bank_name'].widget.attrs['placeholder'] = 'Bank Name'
        self.fields['credit_description'].widget.attrs['placeholder'] = 'Notes (optional)'
        self.fields['credit_interest'].widget.attrs['placeholder'] = '%'
        self.fields['credit_start_date'].widget.attrs['placeholder'] = 'YYYY-MM-DD'
        self.fields['credit_term'].widget.attrs['type'] = 'YYYY-MM-DD'
        self.fields['credit_term'].widget.attrs['placeholder'] = 'YYYY-MM-DD'


class CreditEditForm(CreditAddForm):
    pass


class CreditDeleteForm(CreditBaseForm):
    pass


class CreditPaymentForm(forms.ModelForm):
    class Meta:
        model = CreditPayment
        exclude = ['credit']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.credit = kwargs.pop('credit', None)
        super().__init__(*args, **kwargs)
        self.fields['principal_amount'].widget.attrs['class'] = 'form-control'
        self.fields['interest_amount'].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        payment_date = cleaned_data.get('payment_date')
        if not self.credit:
            raise forms.ValidationError('Credit instance not provided.')
        if payment_date:
            if payment_date < self.credit.credit_start_date:
                raise forms.ValidationError('Payment date must be after the start date of the credit.')
            if payment_date > self.credit.credit_term:
                raise forms.ValidationError('Payment date must be before the end date of the credit.')

        return cleaned_data
