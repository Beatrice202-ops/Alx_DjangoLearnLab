from django.db import models

# Create your models here.
# The Author model represents a book author.
# Each author has a name and can be linked to multiple books.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# The Book model represents a single book.
# Each book has a title, a publication year, and is linked to one author.

class Book(models.Model):
    title = models.CharField(max_length=100)
    publication_year = models.IntegerField
    Author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='book')


    def __str__(self):
        return self.name

