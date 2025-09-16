from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView

# Function-Based View to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-Based View for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context

# User role check functions
def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'member'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'librarian'

def is_admin(user):
    return user.is_superuser

# User role-based views
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            messages.success(request, "Registration successful.")
            return redirect('list_books')  # Redirect to books or home
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm  # You'll need to create this if not already created

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm  # Make sure forms.py exists and has BookForm

# ➕ Add Book View
@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')  # change 'list_books' to your actual view name if different
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Add'})


# ✏️ Edit Book View
@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Edit'})


# ❌ Delete Book View
@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})



