from django.urls import path
from rest_framework_multiauthtoken.views import obtain_auth_token, invalidate_auth_token
from . import views

urlpatterns = [
    path('login', obtain_auth_token),
    path('logout', invalidate_auth_token),
]
