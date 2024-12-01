from rest_framework import serializers
from FixToFlip.offers.models import Offer


class OfferAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
