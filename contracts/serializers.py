from rest_framework import serializers

from django.shortcuts import get_object_or_404

from .models import Contract
from users.models import Saler
from clients.models import Client


class ContractSerializerMethods(serializers.ModelSerializer):
    '''Methods used for contract's serializers.'''

    def get_contract_id(self, instance):
        return instance.id


class ContractSerializer(ContractSerializerMethods):
    '''Serializer of contract.'''

    contract_id = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = [
            'contract_id',
            "title",
            "saler_id",
            "client_id"
            ]


class ContractDetailSerializer(ContractSerializer):
    '''Detail serializer of contract.'''

    saler_first_name = serializers.SerializerMethodField()
    saler_last_name = serializers.SerializerMethodField()
    client_first_name = serializers.SerializerMethodField()
    client_last_name = serializers.SerializerMethodField()
    client_email = serializers.SerializerMethodField()
    client_phone = serializers.SerializerMethodField()
    client_mobil = serializers.SerializerMethodField()
    payment_due = serializers.DateField(
        format="%d-%m-%Y",
        input_formats=['%d-%m-%Y', '%d/%m/%Y', 'iso-8601'])

    class Meta:
        model = Contract
        fields = [
            'contract_id',
            "title",
            "amount",
            "payment_due",
            "signed",
            "saler_id",
            "saler_first_name",
            "saler_last_name",
            'client_id',
            "client_first_name",
            "client_last_name",
            "client_email",
            "client_phone",
            "client_mobil",
            'date_created',
            'date_updated'
            ]

    def get_saler_first_name(self, instance):
        # Get saler first name
        saler = get_object_or_404(Saler, pk=instance.saler.id)
        return saler.first_name

    def get_saler_last_name(self, instance):
        # Get saler last name
        saler = get_object_or_404(Saler, pk=instance.saler.id)
        return saler.last_name

    def get_client_first_name(self, instance):
        # Get client first name
        client = get_object_or_404(Client, pk=instance.client.id)
        return client.first_name

    def get_client_last_name(self, instance):
        # Get client last name
        client = get_object_or_404(Client, pk=instance.client.id)
        return client.last_name

    def get_client_email(self, instance):
        # Get client email
        client = get_object_or_404(Client, pk=instance.client.id)
        return client.email

    def get_client_phone(self, instance):
        # Get client phone
        client = get_object_or_404(Client, pk=instance.client.id)
        return client.phone

    def get_client_mobil(self, instance):
        # Get client mobil
        client = get_object_or_404(Client, pk=instance.client.id)
        return client.mobil
