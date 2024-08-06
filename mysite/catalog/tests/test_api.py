from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from catalog.models import Book
from catalog.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    def test_get(self):
        book_1 = Book.objects.create(
            title="Book_1",
            year=2000,
            summary="Summary book_1",
            isbn=123456789,
            price=100,
        )
        book_2 = Book.objects.create(
            title="Book_2",
            year=2001,
            summary="Summary book_2",
            isbn=123456789,
            price=200,
        )
        url = reverse("book-list")
        response = self.client.get(url)
        serializer_data = BookSerializer([book_1, book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
