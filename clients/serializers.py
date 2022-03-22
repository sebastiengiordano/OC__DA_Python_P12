from rest_framework import serializers

from .models import Client
from users.models import Saler


class ClientSerializerMethods(serializers.ModelSerializer):
    '''Methods used for client's serializers.'''

    def get_client_id(self, instance):
        return instance.id

    def validate(self, data):
        """
        Check if there is at least one field not empty among
        email, phone and mobil.
        """
        if not (
                data.get('email') is not None
                or
                data.get('phone') is not None
                or
                data.get('mobil') is not None):
            raise serializers.ValidationError(
                "At least one field among "
                "email, phone and mobil must be filled.")
        return data


class ClientSerializer(ClientSerializerMethods):
    '''Serializer of client.'''

    client_id = serializers.SerializerMethodField()
    author_user_id = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'client_id',
            "first_name",
            "last_name",
            "company_name",
            "sales_contact_id"
            ]


class ClientDetailSerializer(ClientSerializerMethods):
    '''Detail serializer of client.'''

    saler_first_name = serializers.SerializerMethodField()
    saler_last_name = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'client_id',
            "first_name",
            "last_name",
            "email",
            "phone",
            "mobil",
            "company_name",
            "saler_first_name",
            "saler_last_name",
            'date_created',
            'date_updated'
            ]

    def get_saler_first_name(self, instance):
        # Get saler first name
        queryset = Saler.objects.filter(pk=instance.sales_contact.id)
        saler = queryset[0]
        return saler.first_name

    def get_saler_last_name(self, instance):
        # Get saler last name
        queryset = Saler.objects.filter(pk=instance.sales_contact.id)
        saler = queryset[0]
        return saler.last_name
