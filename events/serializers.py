from rest_framework import serializers

from django.shortcuts import get_object_or_404

from .models import Event
from users.models import Technician
from clients.models import Client
from contracts.models import Contract


class EventSerializerMethods(serializers.ModelSerializer):
    '''Methods used for event's serializers.'''

    def get_event_id(self, instance):
        return instance.id

    def get_client_id(self, instance):
        return instance.client.id

    def get_technician_id(self, instance):
        return instance.technician.id

    def get_contract_id(self, instance):
        return instance.contract.id


class EventSerializer(EventSerializerMethods):
    '''Serializer of event.'''

    event_id = serializers.SerializerMethodField()
    client_id = serializers.SerializerMethodField()
    technician_id = serializers.SerializerMethodField()
    contract_id = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'event_id',
            "title",
            "client_id",
            "technician_id",
            "contract_id"
            ]


class EventDetailSerializer(EventSerializer):
    '''Detail serializer of event.'''

    title = serializers.SerializerMethodField()
    technician_first_name = serializers.SerializerMethodField()
    technician_last_name = serializers.SerializerMethodField()
    client_first_name = serializers.SerializerMethodField()
    client_last_name = serializers.SerializerMethodField()
    client_email = serializers.SerializerMethodField()
    client_phone = serializers.SerializerMethodField()
    client_mobil = serializers.SerializerMethodField()
    attendees = serializers.SerializerMethodField(required=False)
    event_date = serializers.DateField(
        format="%d-%m-%Y",
        input_formats=['%d-%m-%Y', '%d/%m/%Y', 'iso-8601'],
        required=False)
    note = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Event
        fields = [
            'event_id',
            "title",
            "status",
            "attendees",
            "event_date",
            "note",
            'client_id',
            "client_first_name",
            "client_last_name",
            "client_email",
            "client_phone",
            "client_mobil",
            "technician_id",
            "technician_first_name",
            "technician_last_name",
            'date_created',
            'date_updated'
            ]

    def get_title(self, instance):
        # Get contract title
        contract = get_object_or_404(Contract, pk=instance.contract.id)
        return contract.title

    def get_client_first_name(self, instance):
        # Get client first name
        client = get_object_or_404(Client, pk=instance.client.id)
        return client.first_name

    def get_client_first_name(self, instance):
        # Get client first name
        client = get_object_or_404(Client, pk=instance.client.id)
        return client.first_name

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

    def get_technician_first_name(self, instance):
        # Get technician first name
        technician = get_object_or_404(Technician, pk=instance.technician.id)
        return technician.first_name

    def get_technician_last_name(self, instance):
        # Get technician last name
        technician = get_object_or_404(Technician, pk=instance.technician.id)
        return technician.last_name
