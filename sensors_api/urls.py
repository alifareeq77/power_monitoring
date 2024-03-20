from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import user_dashboard, get_sensor_data, ReceiveSensorData, update_switch_status

router = DefaultRouter()
urlpatterns = [
    path('dashboard/<str:dashboard_link>/', user_dashboard, name='user_dashboard'),
    path('api/sensor-data/', get_sensor_data, name='get_sensor_data'),
    path('esp32/receive/<uuid:token>/', ReceiveSensorData.as_view(), name='receive_sensor_data'),
    path('api/update/<uuid:switching_token>/', update_switch_status, name='update_switch_statue'),
    path('', include(router.urls)),
]
