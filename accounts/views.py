from rest_framework import viewsets, mixins
from .models import CustomUser
from .serializers import RegisterSerializer, CommentPostSerializer, LikeCreateSerializer
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




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment, Book
from .serializers import CommentSerializer


class BookCommentsAPIView(APIView):
    def get(self, request):
        book_id = request.GET.get('bookId')
        if not book_id:
            return Response({"error": "bookId query param is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(book=book).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

from rest_framework import generics, permissions


class CreateCommentView(generics.CreateAPIView):
    serializer_class = CommentPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


from .models import Like
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions
class CreateLikeView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # BEFORE calling save, we need to manually check for existing like
        owner = request.user
        comment = serializer.validated_data['comment']

        existing_like = Like.objects.filter(owner=owner, comment=comment).first()

        if existing_like:
            existing_like.delete()
            return Response({'detail': 'Like removed (disliked).'}, status=200)

        # No existing like, now we can create a new one
        serializer.save(owner=owner)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
