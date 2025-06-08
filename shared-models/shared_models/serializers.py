from rest_framework import serializers

class BaseResponseSerializer(serializers.Serializer):
    """統一回應格式"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    data = serializers.JSONField(required=False)