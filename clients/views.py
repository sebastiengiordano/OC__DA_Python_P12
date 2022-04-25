from rest_framework import viewsets

from .models import Client
from .serializers import ClientSerializer, ClientDetailSerializer
from .permissions import ClientPermission


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
    permission_classes = (ClientPermission,)
    filterset_fields = [
        'first_name',
        'last_name',
        'email',
        'company_name',
        'sales_contact_id']
