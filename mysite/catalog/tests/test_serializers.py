from django.test import TestCase

from catalog.models import Book
from catalog.serializers import BookSerializer


class BookSerializersTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(
            title="Book_1",
            year=2000,
            summary="Summary book_1",
            isbn=123456789,
            price=100.50,
        )
        book_2 = Book.objects.create(
            title="Book_2",
            year=2001,
            summary="Summary book_2",
            isbn=987456321,
            price=200.88,
        )
        serializer_data = BookSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                "id": book_1.pk,
                "title": "Book_1",
                "year": "2000",
                "summary": "Summary book_1",
                "isbn": "123456789",
                "price": "100.50",
            },
            {
                "id": book_2.pk,
                "title": "Book_2",
                "year": "2001",
                "summary": "Summary book_2",
                "isbn": "987456321",
                "price": "200.88",
            },
        ]
        self.assertEqual(expected_data, serializer_data)
