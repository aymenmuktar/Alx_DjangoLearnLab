```python
from bookshelf.models import Book

# Retrieve the book you want to delete
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()
# Output: (1, {'bookshelf.Book': 1})

# Confirm deletion
Book.objects.all()
# Output: <QuerySet []>

