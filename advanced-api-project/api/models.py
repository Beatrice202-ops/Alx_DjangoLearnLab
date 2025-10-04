from django.db import models

# Create your models here.
class Author(models.Model):
    """
    Represents an author.
    Fields:
    - name: Author's full name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book.
    Fields:
    - title: The title of the book.
    - publication_year: Year when the book was published.
    - author: Foreign key to Author (one-to-many relation).
    """
    title = models.CharField(max_length=255)
    publication_year = models.PositiveIntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

