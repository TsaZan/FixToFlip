from rest_framework import serializers

from FixToFlip.accounts.models import BaseAccount


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseAccount
        fields = ['__all__']

