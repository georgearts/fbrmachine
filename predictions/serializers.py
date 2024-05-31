from rest_framework import serializers

class PredictSerializer(serializers.Serializer):
    SLA = serializers.FloatField()
    Banda_UP = serializers.FloatField()
    Banda_DOWN = serializers.FloatField()