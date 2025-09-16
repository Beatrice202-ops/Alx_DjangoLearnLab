# Delete Book Example

This file demonstrates how to delete a Book object in Django.

## Example

```python
from bookshelf.models import Book

# Delete a book by ID
book = Book.objects.get(id=1)
book.delete()
```
