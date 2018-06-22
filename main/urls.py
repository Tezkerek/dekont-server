from django.urls import path, include
from rest_framework_multiauthtoken.views import obtain_auth_token, invalidate_auth_token
from rest_framework.routers import DefaultRouter
from . import views

import logging

logger = logging.getLogger(__name__)

groups_router = DefaultRouter()
groups_router.register('groups', views.GroupViewSet, base_name='group')

users_router = DefaultRouter()
users_router.register('users', views.UserViewSet, base_name='user')

urlpatterns = [
    path('login', obtain_auth_token),
    path('logout', invalidate_auth_token),
    path('register', views.RegistrationAPIView.as_view()),
    path('', include(groups_router.urls)),
    path('', include(users_router.urls)),
]
