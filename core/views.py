from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


class HealthCheckResponseSerializer(serializers.Serializer):
    status = serializers.CharField()


@extend_schema(responses=HealthCheckResponseSerializer)
@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"})
