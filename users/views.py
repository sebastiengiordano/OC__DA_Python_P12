from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser, Manager, Saler, Technician
from users.serializers import \
    ManagerSerializer, SalerSerializer, TechnicianSerializer, \
    CustomUserSerializer, CustomUserListSerializer
from users.permissions import IsAdminAuthenticated


class RegisterManagerView(generics.CreateAPIView):
    '''Class which manage the create action for a Manager.'''

    queryset = Manager.objects.all()
    permission_classes = (IsAdminAuthenticated,)
    serializer_class = ManagerSerializer


class RegisterSalerView(generics.CreateAPIView):
    '''Class which manage the create action for a Saler.'''

    queryset = Saler.objects.all()
    permission_classes = (IsAdminAuthenticated,)
    serializer_class = SalerSerializer


class RegisterTechnicianView(generics.CreateAPIView):
    '''Class which manage the create action for a Technician.'''

    queryset = Technician.objects.all()
    permission_classes = (IsAdminAuthenticated,)
    serializer_class = TechnicianSerializer


class UserView(viewsets.GenericViewSet,
               mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin):
    '''Class which manage the
    list, retrieve, update and destroy actions.
    '''
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    list_serializer_class = CustomUserListSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions
        that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAdminAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return super().get_serializer_class()
