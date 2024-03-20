from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserDashboard, SensorData, ESP32Device
from .serializers import SensorDataSerializer


def user_dashboard(request, dashboard_link):
    try:
        user_dashboard = UserDashboard.objects.get(dashboard_link=dashboard_link)
        esp32_device = ESP32Device.objects.filter(user=request.user, name="home")
        context = {'dashboard_link': dashboard_link, "esp32_device": esp32_device}
        return render(request, 'sensors_api/user_dashboard.html', context)
    except UserDashboard.DoesNotExist:
        messages.error(request, 'You do not have access to this dashboard.')
        return redirect('home')  # Redirect to a home page or any other appropriate page


@api_view(['GET'])
@login_required
def get_sensor_data(request):
    user = request.user.id
    try:
        sensor_data = SensorData.objects.filter(user_id=user).latest('timestamp')
        data = {
            'voltage': sensor_data.voltage,
            'current': sensor_data.current,
            'power': sensor_data.power
        }
        return Response(data)
    except SensorData.DoesNotExist:
        return Response({'error': 'Sensor data not found'}, status=404)


@api_view(['PUT'])
@login_required
def update_switch_status(request, switching_token):
    user = request.user.id
    esp32_device = get_object_or_404(ESP32Device, user_id=user, switching_token=switching_token)
    is_switched = request.data.get('is_switched')
    if not str(is_switched):
        return Response({'error': 'switching value is required !'}, status=status.HTTP_400_BAD_REQUEST)
    if not isinstance(is_switched, bool):
        return Response({'error': 'switching value must be boolean !'}, status=status.HTTP_400_BAD_REQUEST)
    print(is_switched)
    esp32_device.is_switched = bool(is_switched)
    esp32_device.save()
    return Response({"is_switched": is_switched}, status=status.HTTP_204_NO_CONTENT)


class ReceiveSensorData(APIView):

    def post(self, request, token):
        esp32_device = get_object_or_404(ESP32Device, token=token)
        voltage = request.data.get('voltage')
        current = float(request.data.get('current')) / 1000
        if not str(voltage) or not str(current):
            return Response({'error': 'Voltage and current values are required'}, status=status.HTTP_400_BAD_REQUEST)

        sensor_data = SensorData.objects.create(user=esp32_device.user, voltage=voltage, current=current)
        serializer = SensorDataSerializer(sensor_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, token):
        esp32_device = get_object_or_404(ESP32Device, token=token)
        is_switched = esp32_device.is_switched
        return Response({'is_switched': is_switched}, status=status.HTTP_200_OK)
