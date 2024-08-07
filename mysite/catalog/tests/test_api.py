from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from catalog.models import Book
from catalog.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.book_1 = Book.objects.create(
            title="Book_1",
            year=2000,
            summary="Summary book_1",
            isbn=123456789,
            price=159,
        )
        self.book_2 = Book.objects.create(
            title="Book_2",
            year=2001,
            summary="Summary book_2",
            isbn=123456789,
            price=159,
        )
        self.book_3 = Book.objects.create(
            title="Book_3",
            year=1999,
            summary="Summary book_3",
            isbn=6255498,
            price=399,
        )

    def test_get(self):
        url = reverse("book-list")
        response = self.client.get(url)
        serializer_data = BookSerializer(
            [self.book_1, self.book_2, self.book_3], many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse("book-list")
        response = self.client.get(url, data={"search": 159})
        serializer_data = BookSerializer([self.book_1, self.book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
