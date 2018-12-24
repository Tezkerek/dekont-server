from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('transactions', views.TransactionViewSet, base_name='transaction')
router.register('categories', views.CategoryViewSet, base_name='category')

urlpatterns = [
    path('', include(router.urls))
]
