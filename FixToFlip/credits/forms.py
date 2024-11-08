from django import forms

from FixToFlip.credits.models import Credit


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
