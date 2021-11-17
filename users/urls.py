from django.urls import path, include
from rest_framework_multiauthtoken.views import obtain_auth_token, invalidate_auth_token, verify_auth_token
from rest_framework.routers import DefaultRouter

from . import views

simple_router = DefaultRouter()
simple_router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('login/', obtain_auth_token),
    path('verify-authtoken/<token>/', verify_auth_token),
    path('logout/', invalidate_auth_token),
    path('register/', views.RegistrationAPIView.as_view()),
    path('', include(simple_router.urls)),
    path('current-user/', views.current_user)
]
