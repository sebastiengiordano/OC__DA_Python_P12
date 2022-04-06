from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Contract
from .serializers import ContractSerializer, ContractDetailSerializer
from .permissions import ContractPermission
from users.permissions import IsAdminAuthenticated, IsSalerAuthenticated


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


class ContractCreateView(mixins.CreateModelMixin,
                         GenericViewSet):
    '''View which manage create action on Contracts.
    '''

    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAdminAuthenticated | IsSalerAuthenticated]
