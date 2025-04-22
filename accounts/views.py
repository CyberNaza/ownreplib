from rest_framework import viewsets, mixins
from .models import CustomUser
from .serializers import RegisterSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer





from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VerifyCodeSerializer

class VerifyCodeView(APIView):

    @swagger_auto_schema(
        request_body=VerifyCodeSerializer,
        responses={200: openapi.Response('User verified successfully'), 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User verified successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



from rest_framework.permissions import IsAuthenticated
from .serializers import MeSerializer

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = MeSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
