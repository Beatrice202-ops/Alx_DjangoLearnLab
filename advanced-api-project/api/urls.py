from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    path('books/', BookListView.as_view(), name="book_list"),
    path('books/create/', BookCreateView.as_view(), name="book_create"),
    path('books/<int:pk>/', BookDetailView.as_view(), name="book_detail"),
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name="book_update"),
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name="book_delete"),
]
