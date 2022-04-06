from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import Contract
from .serializers import ContractSerializer, ContractDetailSerializer
from .permissions import ContractPermission

from users.permissions import IsAdminAuthenticated, IsSalerAuthenticated
from clients.models import Client


class MultipleSerializerMixin:
    '''Class used to set serializer according to action.'''

    detail_serializer_class = None

    def get_serializer_class(self):
        if (
                self.action == 'retrieve'
                and self.detail_serializer_class is not None):
            return self.detail_serializer_class
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

    serializer_class = ContractSerializer
    detail_serializer_class = ContractDetailSerializer
    queryset = Contract.objects.all()
    permission_classes = (ContractPermission,)


class ContractCreateView(APIView):
# class ContractCreateView(generics.CreateAPIView):
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

