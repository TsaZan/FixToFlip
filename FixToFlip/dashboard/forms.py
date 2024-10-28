from django import forms

from FixToFlip.properties.models import Property


class PropertyAddForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'