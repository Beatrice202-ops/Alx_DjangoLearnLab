# Update Book Example

This file demonstrates how to update a Book object in Django.

## Example

```python
from bookshelf.models import Book

# Update a book's title
book = Book.objects.get(id=1)
book.title = "New Title"
book.save()
```
