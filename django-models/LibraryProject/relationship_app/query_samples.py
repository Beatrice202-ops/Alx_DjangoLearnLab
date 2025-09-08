'''Query all books by a specific author.'''
books = Book.objects.filter(author=author)
Author.objects.get(name=author_name)

#list all books in a library
books = library.books.all()
library.object.get(name=library_name)

#Retrieve the librarian for a library.
librarian = library.librarian
Librarian.objects.get(library=library)