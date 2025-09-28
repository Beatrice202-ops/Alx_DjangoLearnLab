from rest_framework import serializers
from .models import Author, Book
from datetime import date

# BookSerializer serializes the Book model.
# It includes custom validation to ensure the publication year is not in the future.

class Bookseralizers(serializers.ModelSerializer):
    class Meta:
        models = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value
    
    # AuthorSerializer serializes the Author model.
# It includes a nested BookSerializer to represent all books written by the author.
# This nested relationship is read-only and allows viewing an author's books.
    class AuthorSerializer(serializers.ModelSerializer):
    # Nest books using BookSerializer, many=True because one author has multiple books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
