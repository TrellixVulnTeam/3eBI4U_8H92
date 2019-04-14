from django.urls import path
from .views import appMenuFinanceiro

urlpatterns = [
    path('', appMenuFinanceiro),
]