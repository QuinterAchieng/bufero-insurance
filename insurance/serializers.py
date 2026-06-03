from rest_framework import serializers
from .models import Customer, Policy


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = [
            "id",
            "policy_type",
            "premium_amount",
            "status",
        ]


class CustomerSerializer(serializers.ModelSerializer):
    policies = PolicySerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "email",
            "wallet_balance",
            "policies",
        ]