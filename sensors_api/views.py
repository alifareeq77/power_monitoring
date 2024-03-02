from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from .models import UserDashboard, SensorData, ESP32Device
from .serializers import SensorDataSerializer
from rest_framework import viewsets
from rest_framework import status
from datetime import timedelta
from django.utils import timezone


def user_dashboard(request, dashboard_link):
    try:
        user_dashboard = UserDashboard.objects.get(dashboard_link=dashboard_link)
        context = {'dashboard_link': dashboard_link}
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


class ReceiveHeartbeat(APIView):
    def post(self, request, token):
        # Retrieve the ESP32 device object based on the token
        esp32_device = get_object_or_404(ESP32Device, token=token)

        # Perform any necessary actions upon receiving a heartbeat
        # For example, you can update a last_seen field on the device object
        esp32_device.update_last_seen()

        return Response(status=status.HTTP_200_OK)


class ESP32DeviceViewSet(viewsets.ViewSet):
    def check_online_status(self, request, token):
        try:
            # Find the ESP32 device with the provided token
            device = ESP32Device.objects.get(token=token)

            # Calculate the time difference between now and the last seen timestamp
            time_difference = timedelta(seconds=300)  # 5 minutes
            is_online = device.last_seen >= (timezone.now() - time_difference)

            # Return the online status
            return Response({'online': is_online}, status=status.HTTP_200_OK)

        except ESP32Device.DoesNotExist:
            # Handle the case where the token is not valid
            return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)
