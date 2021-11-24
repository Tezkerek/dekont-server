from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('transactions', views.TransactionViewSet, basename='transaction')
router.register('categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls))
]
