from django.test import TestCase
from django.contrib.auth import get_user_model

from catalog.loginc import set_rating
from catalog.models import Book, UserBookRelation


class SetRatingTestCase(TestCase):
    def setUp(self) -> None:
        user1 = get_user_model().objects.create(
            username="test_user", first_name="Test1", last_name="User"
        )
        user2 = get_user_model().objects.create(
            username="test_user2", first_name="Test2", last_name="User"
        )
        user3 = get_user_model().objects.create(
            username="test_user3", first_name="Test3", last_name="User"
        )
        self.book_1 = Book.objects.create(
            title="Book_1",
            year=2000,
            summary="Summary book_1",
            isbn=123456789,
            price=100.50,
        )
        UserBookRelation.objects.create(user=user1, book=self.book_1, like=True, rate=4)
        UserBookRelation.objects.create(user=user2, book=self.book_1, like=True, rate=1)
        UserBookRelation.objects.create(user=user3, book=self.book_1, like=True, rate=5)

    def test_ok(self): 
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual("3.33", str(self.book_1.rating))