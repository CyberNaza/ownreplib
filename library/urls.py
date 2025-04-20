from django.urls import path, include
from .views import BookListView




urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    
]
