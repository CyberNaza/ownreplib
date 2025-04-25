from django.urls import path, include
from .views import BookListView, BookDetailView

from django.urls import path
from accounts.views import BookCommentsAPIView



urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    
]
