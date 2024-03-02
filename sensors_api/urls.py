from django.urls import path, include
from .views import user_dashboard, get_sensor_data, ReceiveSensorData, ReceiveHeartbeat
from .views import ESP32DeviceViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'esp32', ESP32DeviceViewSet, basename='esp32')
urlpatterns = [
    path('dashboard/<str:dashboard_link>/', user_dashboard, name='user_dashboard'),
    path('api/sensor-data/', get_sensor_data, name='get_sensor_data'),
    path('esp32/receive/<uuid:token>/', ReceiveSensorData.as_view(), name='receive_sensor_data'),
    path('esp32/receive/<uuid:token>/heartbeat/', ReceiveHeartbeat.as_view(), name='receive_heartbeat'),
    path('', include(router.urls)),
]
