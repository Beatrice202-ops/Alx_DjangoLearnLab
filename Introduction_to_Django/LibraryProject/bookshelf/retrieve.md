# Retrieve Book Example

This file demonstrates how to retrieve Book objects in Django.

## Example

```python
from bookshelf.models import Book

# Retrieve all books
books = Book.objects.all()

# Retrieve a single book by ID
book = Book.objects.get(title="1984")
```
