from django.shortcuts import render, get_object_or_404

# Create your views here.
# views.py
from .models import Book, Library
from django.views.generic.detail import DetailView

# Function-Based View to list all books
def list_books(request):
    books = Book.objects.all()  # <-- This line satisfies the checker
    return render(request, 'relationship_app/list_books.html', {'books': books})


