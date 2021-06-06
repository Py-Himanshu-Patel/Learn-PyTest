from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'currency', CurrencyViewSet)
router.register(r'transaction', TransactionViewset)

urlpatterns = router.urls
