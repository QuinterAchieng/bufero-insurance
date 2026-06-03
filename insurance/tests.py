from django.test import TestCase
from .services import calculate_premium_logic

from decimal import Decimal
from .views import calculate_premium


class PremiumCalculatorTests(TestCase):

    def test_age_under_25_motorcycle(self):
        premium = calculate_premium_logic(
            age=20,
            vehicle_type="motorcycle",
            accidents=0
        )
        self.assertEqual(premium, 70)

    def test_car_no_accidents(self):
        premium = calculate_premium_logic(
            age=30,
            vehicle_type="car",
            accidents=0
        )
        self.assertEqual(premium, 70)

    def test_scooter_with_accidents(self):
        premium = calculate_premium_logic(
            age=40,
            vehicle_type="electric_scooter",
            accidents=3
        )
        self.assertEqual(premium, 90)
