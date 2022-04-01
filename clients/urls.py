from django.urls import path, include

from rest_framework import routers

from .views import ClientView

router = routers.SimpleRouter()
router.register('clients', ClientView, basename='clients')

app_name = 'clients'
urlpatterns = [
    # For managed all Client's action
    # (create, list, retrieve, update, destroy)
    path('', include(router.urls)),
]
