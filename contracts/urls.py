from django.urls import path, include

from rest_framework import routers

from .views import ContractView

router = routers.SimpleRouter()
router.register('contracts', ContractView, basename='contracts')

app_name = 'contracts'
urlpatterns = [
    # For managed all Contract's action
    # (create, list, retrieve, update, destroy)
    path('', include(router.urls)),
]
