# tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import SensorData, UserDashboard

User = get_user_model()


class SensorDataTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@test', password='password')

    def test_sensor_data_creation(self):
        sensor_data = SensorData.objects.create(user=self.user, voltage=5.0, current=2.0)
        self.assertEqual(sensor_data.user, self.user)
        self.assertEqual(sensor_data.voltage, 5.0)
        self.assertEqual(sensor_data.current, 2.0)
        self.assertEqual(sensor_data.power, 10.0)  # Check if power is calculated correctly


class UserDashboardTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@test', password='password')

    def test_user_dashboard_creation(self):
        user_dashboard = UserDashboard.objects.get(user=self.user)
        self.assertEqual(user_dashboard.user, self.user)
        self.assertTrue(len(user_dashboard.dashboard_link) > 0)  # Check if dashboard link is generated
