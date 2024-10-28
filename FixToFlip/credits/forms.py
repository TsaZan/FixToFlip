from django import forms

from FixToFlip.credits.models import Credit


class CreditBaseForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = '__all__'


class CreditAddForm(CreditBaseForm):
    pass


class CreditEditForm(CreditBaseForm):
    pass


class CreditDeleteForm(CreditBaseForm):
    pass
