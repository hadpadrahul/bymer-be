from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.registry import get_entry


class AdminAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]
    renderer_classes = [JSONRenderer]


class AdminHealthView(AdminAPIView):
    def get(self, request):
        return Response({"status": "ok", "user": request.user.username})


class ToggleActiveView(AdminAPIView):
    def patch(self, request, registry_key, pk):
        entry = get_entry(registry_key)
        obj = entry.model.objects.filter(pk=pk).first()
        if obj is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if not hasattr(obj, "is_active"):
            return Response({"detail": "Not supported."}, status=status.HTTP_400_BAD_REQUEST)
        obj.is_active = not obj.is_active
        obj.save(update_fields=["is_active"])
        return Response({"id": obj.pk, "is_active": obj.is_active})


class UpdateOrderView(AdminAPIView):
    def patch(self, request, registry_key, pk):
        entry = get_entry(registry_key)
        obj = entry.model.objects.filter(pk=pk).first()
        if obj is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if not hasattr(obj, "order"):
            return Response({"detail": "Not supported."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = int(request.data.get("order", obj.order))
        except (TypeError, ValueError):
            return Response({"detail": "Invalid order."}, status=status.HTTP_400_BAD_REQUEST)
        obj.order = order
        obj.save(update_fields=["order"])
        return Response({"id": obj.pk, "order": obj.order})
