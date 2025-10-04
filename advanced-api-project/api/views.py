from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# GET /api/books/
class ListView(generics.ListAPIView):
    """
    Lists all books. Public access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# GET /api/books/<pk>/
class DetailView(generics.RetrieveAPIView):
    """
    Retrieves a single book by ID. Public access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# POST /api/books/create/
class CreateView(generics.CreateAPIView):
    """
    Creates a new book. Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# PUT/PATCH /api/books/<pk>/update/
class UpdateView(generics.UpdateAPIView):
    """
    Updates an existing book. Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# DELETE /api/books/<pk>/delete/
class DeleteView(generics.DestroyAPIView):
    """
    Deletes a book. Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

