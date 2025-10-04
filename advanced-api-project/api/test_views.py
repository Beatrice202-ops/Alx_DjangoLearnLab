from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a user to test authentication-restricted endpoints
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()

        # Create an author and some books
        self.author = Author.objects.create(name="John Doe")
        self.book1 = Book.objects.create(title="Book One", publication_year=2001, author=self.author)
        self.book2 = Book.objects.create(title="Book Two", publication_year=2020, author=self.author)

        # URLs for convenience
        self.book_list_url = reverse('book-list')
        self.book_create_url = reverse('book-create')
        self.book_detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})
        self.book_update_url = lambda pk: reverse('book-update', kwargs={'pk': pk})
        self.book_delete_url = lambda pk: reverse('book-delete', kwargs={'pk': pk})

    def test_list_books(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two books exist

    def test_filter_books_by_title(self):
        response = self.client.get(self.book_list_url, {'title': 'Book One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    def test_search_books(self):
        response = self.client.get(self.book_list_url, {'search': 'Two'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book Two')

    def test_order_books(self):
        response = self.client.get(self.book_list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the first book has the latest publication year
        self.assertEqual(response.data[0]['publication_year'], 2020)

    def test_create_book_unauthenticated(self):
        # Should fail because create requires auth
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')

    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'Updated Title',
            'publication_year': 2021,
            'author': self.author.id
        }
        response = self.client.put(self.book_update_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_update_book_unauthenticated(self):
        data = {
            'title': 'Should Not Update',
            'publication_year': 2021,
            'author': self.author.id
        }
        response = self.client.put(self.book_update_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(self.book_delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_book_unauthenticated(self):
        response = self.client.delete(self.book_delete_url(self.book2.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Book.objects.filter(id=self.book2.id).exists())
