from django.urls import path, include

from rest_framework import routers

from .views import ContractView, ContractCreateView

router = routers.SimpleRouter()
router.register('contracts', ContractView, basename='contracts')

app_name = 'contracts'
urlpatterns = [
    # For managed the following Contract's action:
    # list, retrieve, update, destroy
    path('', include(router.urls)),
    # For managed Contract create action
    path(
        'clients/<int:client_id>/contracts/',
        ContractCreateView.as_view(),
        name='create_contracts'),
]
