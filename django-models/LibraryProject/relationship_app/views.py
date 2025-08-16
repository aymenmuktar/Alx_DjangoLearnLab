from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library

# Function-based View: List all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/templates/list_books.html', {'books': books})

# Class-based View: Display details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/templates/library_detail.html'
    context_object_name = 'library'

