from django.urls import path, include

from rest_framework import routers

from .views import EventView, EventCreateView

router = routers.SimpleRouter()
router.register('events', EventView, basename='events')

app_name = 'events'
urlpatterns = [
    # For managed the following Event's action:
    # list, retrieve, update, destroy
    path('', include(router.urls)),
    # For managed Event create action
    path(
        'contracts/<int:contract_id>/events/',
        EventCreateView.as_view(),
        name='create_events'),
]
