from cloudinary.forms import CloudinaryJsFileField
from django import forms

from FixToFlip.blog.models import BlogPost
from FixToFlip.properties.models import Property
from FixToFlip.validators import get_current_date, get_current_year


class PropertyAddForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['owner']

        widgets = {
            'image': CloudinaryJsFileField(attrs={
                'class': 'dash-input-wrapper mb-20 attached-file d-flex align-items-center justify-content-between '
                         'mb-15'
            }),
            'bought_date': forms.DateInput(attrs={
                'type': 'date',
                'max': get_current_date(),
                'min': '1900-01-01'
            }),
            'property_size': forms.TextInput(attrs={'placeholder': 'Ex: 1,230 sqm'}),
            'property_price': forms.TextInput(attrs={'placeholder': 'Ex: 1,230,000'}),
            'bedrooms': forms.NumberInput(attrs={'placeholder': 'Ex: 3', }),
            'bathrooms': forms.NumberInput(attrs={'placeholder': 'Ex: 2', }),
            'year_of_built': forms.NumberInput(attrs={'placeholder': 'Ex: 2000', 'min': '1900', 'max': get_current_year()}),
        }



