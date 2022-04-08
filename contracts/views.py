from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet, generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404

from .models import Contract
from .serializers import ContractSerializer, ContractDetailSerializer
from .permissions import ContractPermission

from users.permissions import IsAdminAuthenticated, IsSalerAuthenticated
from clients.models import Client


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


class ContractView(MultipleSerializerMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    '''View which manage retrieve, update,
    destroy and list actions on Contracts.
    '''

    serializer_class = ContractDetailSerializer
    list_serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = (ContractPermission,)


class ContractCreateView(generics.CreateAPIView):
    '''View which manage create action on Contracts.'''

    permission_classes = [IsAdminAuthenticated | IsSalerAuthenticated]

    def post(self, request, client_id):
        """
        Create a contract.
        """

        # Check if request data is valid
        serializer = ContractDetailSerializer(data=request.data)
        if serializer.is_valid():
            # Get client by id
            client = get_object_or_404(Client, pk=client_id)
            # Check if the saler is in contact with this client
            self.check_if_saler_in_contact_with_client(request.user, client)
            # Create the contract
            contract = Contract.objects.create(
                title=serializer.validated_data['title'],
                saler=request.user,
                client=client,
                amount=serializer.validated_data['amount'],
                payment_due=serializer.validated_data['payment_due'])
            serializer = ContractSerializer(contract)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_if_saler_in_contact_with_client(self, saler, client):
        clients_of_saler = Client.objects.filter(sales_contact=saler)
        if client not in clients_of_saler:
            raise PermissionDenied(
                detail=(
                    'Method post is not allowed since you\'re '
                    'not the saler in contact with this client.')
                )
