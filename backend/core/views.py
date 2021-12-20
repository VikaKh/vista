from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core import swagger
from core.models import Review
from core.serializers import AuthResponseSerializer, RegisterRequestSerializer, ReviewSerializer


class Login(ObtainAuthToken):
    @swagger_auto_schema(**swagger.login_schema)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(AuthResponseSerializer(user).data, status=200)


class Register(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(**swagger.register_schema)
    def post(self, request):
        serializer = RegisterRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(AuthResponseSerializer(user).data, status=201)


class ReviewView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
