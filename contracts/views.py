from rest_framework import viewsets

from .models import Contract
from .serializers import ContractSerializer, ContractDetailSerializer
from .permissions import ContractPermission


class MultipleSerializerMixin:
    '''Class used to set serializer according to action.'''

    detail_serializer_class = None

    def get_serializer_class(self):
        if (
                self.action == 'retrieve'
                and self.detail_serializer_class is not None):
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContractView(MultipleSerializerMixin, viewsets.ModelViewSet):
    '''View which manage all actions on Contracts.'''

    serializer_class = ContractSerializer
    detail_serializer_class = ContractDetailSerializer
    queryset = Contract.objects.all()
    permission_classes = (ContractPermission,)
