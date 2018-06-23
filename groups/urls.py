from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

simple_router = DefaultRouter()
simple_router.register('groups', views.GroupViewSet, base_name='group')

urlpatterns = [
    path('', include(simple_router.urls))
]
