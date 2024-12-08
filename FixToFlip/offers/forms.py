from django import forms
from djmoney.forms import MoneyField

from FixToFlip.choices import PublishChoices
from FixToFlip.offers.models import Offer
from FixToFlip.properties.forms import PropertyBaseForm
from FixToFlip.properties.models import Property


class OfferBaseForm(forms.ModelForm):
    listed_price = MoneyField(
        decimal_places=2,
        max_digits=10,
        default_currency="EUR",
        required=False,
    )

    class Meta:
        model = Offer
        fields = [
            "title",
            "featured_image",
            "description",
            "listed_price",
            "offer_status",
            "listed_property",
            "is_published",
        ]

        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4, "placeholder": "Enter offer details...",
            }),
            "title": forms.TextInput(attrs={
                "placeholder": "Offer Title",
            }),
            'is_published': forms.Select(choices=PublishChoices.choices,
                                         attrs={'class': 'form-control'}),

        }


class OfferAddForm(OfferBaseForm):
    pass


class OfferEditForm(OfferBaseForm):
    class Meta:
        model = Offer
        exclude = ['listed_property',
                   ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4, "placeholder": "Enter offer details...",
            }),

            "title": forms.TextInput(attrs={
                "placeholder": "Offer Title",
            }),
        }


class PropertyOfferEditForm(PropertyBaseForm):
    class Meta:
        model = Property
        exclude = ['owner',
                   'property_name',
                   'property_description',
                   'bought_date',
                   ]


class OfferDeleteForm(OfferBaseForm):
    pass
