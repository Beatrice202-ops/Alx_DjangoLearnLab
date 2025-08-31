# Create Book Example

This file demonstrates how to create a Book object in Django.

## Example

```python
from bookshelf.models import Book

# Create a new book
Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```
