from django.urls import path, include

from rest_framework import routers

from .views import ContractView, ContractCreateView

router = routers.SimpleRouter()
router.register('contracts', ContractView, basename='contracts')
# router.register('clients/<int:client_id>/', ContractCreateView, basename='contracts')

app_name = 'contracts'
urlpatterns = [
    # For managed all Contract's action
    # (create, list, retrieve, update, destroy)
    path('', include(router.urls)),
    path(
        'contracts/clients/<int:client_id>/',
        ContractCreateView.as_view(),
        name='create_contracts'),
]
