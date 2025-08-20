from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView

# =======================
# Role-Based Access Views
# =======================

# Helper functions for role checking
def is_admin(user):
    return hasattr(user, 'profile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'profile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'profile') and user.userprofile.role == 'Member'

# Admin view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, '/relationship_app/admin_view.html')

# Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member view
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


# =======================
# Book & Library Views
# =======================

# Function-based View: List all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based View: Display details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# -----------------------
# Step 2: Secured Book CRUD
# -----------------------

# Add Book
@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')  # redirect to your books list
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})


# Edit Book
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
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})


# Delete Book
@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})



# =====================
# Authentication Views
# =====================

# Registration view
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            return redirect("home")  # Change "home" to your homepage route
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# Login view (using Django’s built-in)
class CustomLoginView(LoginView):
    template_name = "relationship_app/login.html"


# Logout view
def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")

