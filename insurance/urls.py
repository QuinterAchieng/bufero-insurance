from django.urls import path
from .views import create_customer, calculate_premium, get_customer, create_claim, renew_policy

urlpatterns = [
     path('customers/', create_customer),
     path('customers/<int:pk>/', get_customer),
     path('calculate-premium/', calculate_premium),
     path('claims/', create_claim),
     path('renew-policy/', renew_policy),
]