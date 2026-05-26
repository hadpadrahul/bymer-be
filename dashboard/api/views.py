from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class AdminAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]
    renderer_classes = [JSONRenderer]


class AdminHealthView(AdminAPIView):
    def get(self, request):
        return Response({"status": "ok", "user": request.user.username})
