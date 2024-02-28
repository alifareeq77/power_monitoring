from rest_framework import serializers

from sensors_api.models import Current, Voltage, Power


class CurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Current
        fields = "__all__"


class VoltageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voltage
        fields = '__all__'


class PowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Power
        fields = "__all__"


class CombinedSerializer(serializers.Serializer):
    current = CurrentSerializer()
    voltage = VoltageSerializer()
    power = PowerSerializer()


class HeartbeatSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    # Add any other fields you need from the heartbeat request
