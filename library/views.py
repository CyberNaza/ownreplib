from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from .models import Book
from .serializers import BookSerializer
from accounts.models import Book, Comment, Like
from accounts.serializers import BookSerializer, CommentSerializer, LikeSerializer
from rest_framework.permissions import AllowAny
class BookPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookListView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = BookPagination
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', None)
        
        if search_query:
            books = Book.objects.filter(name__icontains=search_query)
        else:
            books = Book.objects.all()
        
        # Initialize paginator and get paginated response
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(books, request)
        
        if page is not None:
            serializer = BookSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # Fallback if pagination is disabled
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookDetailView(APIView):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(book=book).order_by('-created_at')
        likes = Like.objects.filter(comment__book=book)

        book_data = BookSerializer(book).data
        comment_data = CommentSerializer(comments, many=True).data
        like_data = LikeSerializer(likes, many=True).data

        return Response({
            'book': book_data,
            'comments': comment_data,
            'likes': like_data
        })
