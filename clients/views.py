from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Client
from .serializers import ClientSerializer, ClientDetailSerializer
from .permissions import ClientPermission
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


class ClientView(MultipleSerializerMixin, viewsets.ModelViewSet):
    '''View which manage all actions on clients.'''

    serializer_class = ClientSerializer
    detail_serializer_class = ClientDetailSerializer
    queryset = Client.objects.all()
    permission_classes = [ClientPermission | IsAdminAuthenticated]


    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of
    #     permissions that this view require.
    #     """
    #     if self.action == 'create':
    #         permission_classes = (IsAuthenticated,)
    #     else:
    #         permission_classes = (ClientPermission,)
    #     return [permission() for permission in permission_classes]
