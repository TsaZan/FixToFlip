from rest_framework import serializers
from FixToFlip.credits.models import Credit



class CreditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Credit
        fields = ['__all__']
