import rest_framework.routers
from django.urls import path
from sensors_api import views
from sensors_api.views import CombinedDataView, HeartbeatView

router = rest_framework.routers.SimpleRouter()
router.register(r'voltage', views.VoltageViewSet, basename='voltage')
router.register(r'voltage', views.CurrentViewSet, basename='current')
router.register(r'voltage', views.PowerViewSet, basename='power')

urlpatterns = [path('combined-data/', CombinedDataView.as_view(), name='combined-data'),
               path('heartbeat/', HeartbeatView.as_view(), name='heartbeat')
               ] + router.urls
