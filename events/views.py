from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet, generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404

from .models import Event
from .serializers import \
    EventSerializer, EventDetailSerializer, \
    EventCreateSerializer, EventUpdateSerializer
from .permissions import EventPermission

from users.models import Technician
from users.permissions import IsAdminAuthenticated, IsSalerAuthenticated
from clients.models import Client
from contracts.models import Contract


class MultipleSerializerMixin:
    '''Class used to set serializer according to action.'''

    list_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return EventSerializer
        if self.action == 'update':
            return EventUpdateSerializer
        return EventDetailSerializer


class EventView(MultipleSerializerMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    '''View which manage retrieve, update,
    destroy and list actions on Events.
    '''

    queryset = Event.objects.all()
    permission_classes = (EventPermission,)
    filterset_fields = {
        'client_id': ['exact'],
        'technician_id': ['exact'],
        'contract_id': ['exact'],
        'status': ['exact'],
        'event_date':['gte', 'lte', 'exact', 'gt', 'lt']}

    def update(self, request, pk):
        """
        Create an event.
        """
        # Check if request data is valid
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            # Get event by id
            event = get_object_or_404(Event, pk=pk)
            # Check if the user manage this event
            self.check_if_user_manage_this_event(request.user, event)
            # Get technican by email or keep the one in event
            email = serializer.validated_data.get('technician_email')
            if email is not None:
                technician = Technician.objects.filter(email=email)
            else:
                technician = event.technician
            # Update the event
            event.technician = technician
            event.status = (
                serializer.validated_data.get('status')
                or event.status)
            event.attendees = (
                serializer.validated_data.get('attendees')
                or event.attendees)
            event.event_date = (
                serializer.validated_data.get('event_date')
                or event.event_date)
            event.note = (
                serializer.validated_data.get('note')
                or event.note)
            event.save()
            serializer = EventDetailSerializer(
                get_object_or_404(Event, pk=pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_if_user_manage_this_event(self, user, event: Event):
        saler = event.contract.saler
        technician = event.technician
        if user not in (saler, technician):
            raise PermissionDenied(
                detail=(
                    'Method put is not allowed since '
                    'you\'re not in contact with this client.')
                )


class EventCreateView(generics.CreateAPIView):
    '''View which manage create action on Events.'''

    permission_classes = [IsAdminAuthenticated | IsSalerAuthenticated]

    def post(self, request, contract_id):
        """
        Create an event.
        """

        # Check if request data is valid
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Get contract by id
            contract = get_object_or_404(Contract, pk=contract_id)
            # Get technican by email
            email = serializer.validated_data['technician_email']
            technician = get_object_or_404(
                Technician,
                email=email)
            # Check if the user is in contact with this client
            self.check_if_user_in_contact_with_client(
                request.user, contract.client)
            # Check if the user manage this contract
            self.check_if_user_manage_this_contract(request.user, contract)
            # Create the event
            event = Event.objects.create(
                client=contract.client,
                technician=technician,
                contract=contract,
                attendees=serializer.validated_data.get('attendees'),
                event_date=serializer.validated_data.get('event_date'),
                note=serializer.validated_data.get('note'))
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_if_user_in_contact_with_client(self, user, client: Client):
        clients_of_user = Client.objects.filter(sales_contact=user)
        if client not in clients_of_user:
            raise PermissionDenied(
                detail=(
                    'Method post is not allowed since '
                    'you\'re not in contact with this client.')
                )

    def check_if_user_manage_this_contract(self, user, contract: Contract):
        contracts_of_user = Contract.objects.filter(saler=user)
        if contract not in contracts_of_user:
            raise PermissionDenied(
                detail=(
                    'Method post is not allowed since you\'re '
                    'not the user who manage this cotract.')
                )
