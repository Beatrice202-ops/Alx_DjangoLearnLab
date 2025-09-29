from django.db import models

# Create your models here.
from datetime import datetime

class Author(models.Model):
    """
    Author model represents a writer with a name.
    Each Author can have multiple related Book entries (one-to-many).
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Book model represents a published book with a title, publication year,
    and a foreign key linking to an Author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title

