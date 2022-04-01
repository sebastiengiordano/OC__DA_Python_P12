from rest_framework import serializers

from .models import Client
from users.models import Saler


class ClientSerializerMethods(serializers.ModelSerializer):
    '''Methods used for client's serializers.'''

    def create(self, validated_data):
        """Creates and saves a Client."""

        # Get the current user
        user = self.context['request'].user
        # Create the client
        return Client.objects.create(
            sales_contact=user,
            **validated_data)

    def get_client_id(self, instance):
        return instance.id

    def validate(self, data):
        """
        Check if there is at least one field not empty among
        email, phone and mobil.
        And append it/them in data.

        Moreover, manage client update.
        """

        # Get data from request
        request_data = self.context['request'].data
        email = request_data.get('email')
        phone = request_data.get('phone')
        mobil = request_data.get('mobil')
        # Check if client already exist (update in progress)
        if self.instance is not None:
            # Keep instance value if no updated value, and
            # manage the case when user want to delete an invalid entry
            email = '' if email == '' else email or self.instance.email
            phone = '' if phone == '' else phone or self.instance.phone
            mobil = '' if mobil == '' else mobil or self.instance.mobil
        # Check if there is at least one field
        # not empty among email, phone and mobil.
        if not (
                email is not None
                or
                phone is not None
                or
                mobil is not None):
            raise serializers.ValidationError(
                "At least one field among "
                "email, phone and mobil must be filled.")
        # Append request's data in data
        data['email'] = email or ''
        data['phone'] = phone or ''
        data['mobil'] = mobil or ''
        return data


class ClientSerializer(ClientSerializerMethods):
    '''Serializer of client.'''

    client_id = serializers.SerializerMethodField()

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

    client_id = serializers.SerializerMethodField()
    saler_first_name = serializers.SerializerMethodField()
    saler_last_name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'client_id',
            "first_name",
            "last_name",
            "email",
            "phone",
            "mobil",
            "company_name",
            "sales_contact_id",
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
