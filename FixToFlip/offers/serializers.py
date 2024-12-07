from rest_framework import serializers

from FixToFlip.accounts.models import BaseAccount
from FixToFlip.offers.models import Offer
from FixToFlip.properties.models import Property


class OfferPublisherSerializer(serializers.ModelSerializer):
    profile_type = serializers.CharField(
        source='profile.profile_type',
        allow_null=True,
    )

    class Meta:
        model = BaseAccount
        fields = ('profile_type',)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if data['profile_type'] == 'Personal':
            data['profile_name'] = instance.profile.user.first_name + ' ' + instance.profile.user.last_name
            data['phone_number'] = str(instance.profile.phone_number)

        else:
            data['company_name'] = instance.profile.company_name
            data['company_phone'] = str(instance.profile.company_phone)

        return data


class OfferedPropertySerializer(serializers.ModelSerializer):
    seller = OfferPublisherSerializer(source='owner')

    class Meta:
        model = Property
        fields = ['country',
                  'city',
                  'address',
                  'property_type',
                  'year_of_built',
                  'property_size',
                  'floor',
                  'bedrooms',
                  'bathrooms',
                  'seller',
                  ]


class OfferAPISerializer(serializers.ModelSerializer):
    listed_property = OfferedPropertySerializer()

    class Meta:
        model = Offer
        exclude = ['is_published',
                   'updated_at',
                   'created_at',
                   'actual_sold_price',
                   'actual_sold_price_currency',
                   'sold_date'
                   ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        featured_image_url = (
            instance.featured_image.url if instance.featured_image else None
        )
        offer_data = {
            "id": data.get("id"),
            "title": data.get("title"),
            "featured_image": featured_image_url,
            "description": data.get("description"),
            "listed_price_currency": data.get("listed_price_currency"),
            "listed_price": data.get("listed_price"),
            "offer_status": data.get("offer_status"),
            "listed_property": data.get("listed_property"),
        }

        return offer_data
