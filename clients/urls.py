from django.urls import path, include

from rest_framework import routers

from .views import ClientView

router = routers.SimpleRouter()
router.register('client', ClientView, basename='client')

app_name = 'clients'
urlpatterns = [
    # For managed all Clients (all action: create, list, retrieve, update, destroy)
    path('', include(router.urls)),
]
