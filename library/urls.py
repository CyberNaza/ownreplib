from django.urls import path, include
from .views import BookListView, BookDetailView

from django.urls import path
from accounts.views import *



urlpatterns = [
    path('comments/create/', CreateCommentView.as_view(), name='comment-create'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('likes/create/', CreateLikeView.as_view(), name='like-create'),
    
]
