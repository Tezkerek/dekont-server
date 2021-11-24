from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

simple_router = DefaultRouter()
simple_router.register('groups', views.GroupViewSet, basename='group')

urlpatterns = [
    path('', include(simple_router.urls)),
    path('current-group/', views.current_user_group),
]
