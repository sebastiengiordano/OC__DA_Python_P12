from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet, generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404

from .models import Event
from .serializers import EventSerializer, EventDetailSerializer
from .permissions import EventPermission

from users.models import Technician
from users.permissions import IsAdminAuthenticated, IsSalerAuthenticated
from clients.models import Client
from contracts.models import Contract


class MultipleSerializerMixin:
    '''Class used to set serializer according to action.'''

    list_serializer_class = None
    action_for_list_serializer = ('list', 'create')

    def get_serializer_class(self):
        if (
                self.action in self.action_for_list_serializer
                and self.list_serializer_class is not None):
            return self.list_serializer_class
        return super().get_serializer_class()


class EventView(MultipleSerializerMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    '''View which manage retrieve, update,
    destroy and list actions on Events.
    '''

    serializer_class = EventDetailSerializer
    list_serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = (EventPermission,)


class EventCreateView(generics.CreateAPIView):
    '''View which manage create action on Events.'''

    permission_classes = [IsAdminAuthenticated | IsSalerAuthenticated]

    def post(self, request, contract_id):
        """
        Create an event.
        """

        # Check if request data is valid
        serializer = EventDetailSerializer(data=request.data)
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
                attendees=serializer.validated_data['attendees'],
                event_date=serializer.validated_data['event_date'],
                note=serializer.validated_data['note'])
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_if_user_in_contact_with_client(self, user, client):
        clients_of_user = Client.objects.filter(sales_contact=user)
        if client not in clients_of_user:
            raise PermissionDenied(
                detail=(
                    'Method post is not allowed since you\'re '
                    'not the user in contact with this client.')
                )

    def check_if_user_manage_this_contract(self, user, contract):
        contracts_of_user = Contract.objects.filter(saler=user)
        if contract not in contracts_of_user:
            raise PermissionDenied(
                detail=(
                    'Method post is not allowed since you\'re '
                    'not the user who manage this cotract.')
                )
