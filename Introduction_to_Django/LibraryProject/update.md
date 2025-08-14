# Update title
book.title = "Nineteen Eighty-Four"
book.save()

# Confirm update
book = Book.objects.get(id=book.id)
book.title
# Output: 'Nineteen Eighty-Four'

