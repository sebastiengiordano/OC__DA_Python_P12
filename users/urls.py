from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import \
    TokenObtainPairView, TokenRefreshView

from users.views import UserView, \
    RegisterManagerView, RegisterSalerView, RegisterTechnicianView
router = routers.SimpleRouter()
router.register('user', UserView, basename='user')

app_name = 'users'
urlpatterns = [
    # For JWT tokens management
    path('login/',
         TokenObtainPairView.as_view(),
         name='login'),
    path('token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    # For register a new User (which could be a Manager, Saler or Technician)
    path('register/manager/',
         RegisterManagerView.as_view(),
         name='register_manager'),
    path('register/saler/',
         RegisterSalerView.as_view(),
         name='register_saler'),
    path('register/technician/',
         RegisterTechnicianView.as_view(),
         name='register_technician'),
    # For managed all CustomUsers (action: list, retrieve, update, destroy)
    path('', include(router.urls)),
]
