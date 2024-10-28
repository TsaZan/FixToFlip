from django import forms

from FixToFlip.offers.models import Offer


class OfferBaseForm(forms.ModelForm):
    pass

    class Meta:
        model = Offer
        fields = '__all__'


class OfferAddForm(OfferBaseForm):
    pass


class OfferEditForm(OfferBaseForm):
    pass


class OfferDeleteForm(OfferBaseForm):
    pass
