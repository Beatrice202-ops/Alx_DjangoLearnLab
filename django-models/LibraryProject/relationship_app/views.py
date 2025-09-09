from django.shortcuts import render, get_object_or_404

# Create your views here.
# views.py
from .models import Book, Library
from django.views.generic.detail import DetailView

# Function-Based View to list all books
def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-Based View for Library Detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


