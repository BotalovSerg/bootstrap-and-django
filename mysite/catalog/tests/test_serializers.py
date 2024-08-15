from django.test import TestCase
from django.db.models import Count, Case, When, Avg
from django.contrib.auth import get_user_model

from catalog.models import Book, UserBookRelation
from catalog.serializers import BookSerializer


class BookSerializersTestCase(TestCase):
    def test_ok(self):
        user1 = get_user_model().objects.create(username="test_user")
        user2 = get_user_model().objects.create(username="test_user2")
        user3 = get_user_model().objects.create(username="test_user3")
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
        UserBookRelation.objects.create(user=user1, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user1, book=book_2, like=True, rate=4)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False, rate=3)

        books = Book.objects.annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg("userbookrelation__rate"),
        ).order_by("id")
        serializer_data = BookSerializer(books, many=True).data
        expected_data = [
            {
                "id": book_1.pk,
                "title": "Book_1",
                "year": "2000",
                "summary": "Summary book_1",
                "isbn": "123456789",
                "price": "100.50",
                "likes_count": 3,
                "annotated_likes": 3,
                "rating": "5.00",
            },
            {
                "id": book_2.pk,
                "title": "Book_2",
                "year": "2001",
                "summary": "Summary book_2",
                "isbn": "987456321",
                "price": "200.88",
                "likes_count": 1,
                "annotated_likes": 1,
                "rating": "3.50",
            },
        ]
        self.assertEqual(expected_data, serializer_data)
