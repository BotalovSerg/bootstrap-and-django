import json

from django.db.models import Count, Case, When, Avg
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from catalog.models import Book, UserBookRelation
from catalog.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(username="test_user")
        self.book_1 = Book.objects.create(
            title="Book_1",
            year=2000,
            summary="Summary book_1",
            isbn=123456789,
            price=159,
            owner=self.user,
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
        UserBookRelation.objects.create(
            user=self.user, book=self.book_1, like=True, rate=5
        )

    def test_get(self):
        url = reverse("book-list")
        response = self.client.get(url)
        books = Book.objects.annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
        ).order_by("id")
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]["rating"], "5.00")
        # self.assertEqual(serializer_data[0]["likes_count"], 1)
        self.assertEqual(serializer_data[0]["annotated_likes"], 1)

    def test_get_search(self):
        url = reverse("book-list")
        books = (
            Book.objects.filter(pk__in=[self.book_1.pk, self.book_2.pk])
            .annotate(
                annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            )
            .order_by("id")
        )
        response = self.client.get(url, data={"search": 159})
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_created(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse("book-list")
        data = {
            "title": "Book Python",
            "year": 2023,
            "summary": "Summary Book Python",
            "isbn": 123456789,
            "price": 555.00,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, json_data, content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse("book-detail", kwargs={"pk": self.book_1.pk})
        data = {
            "title": self.book_1.title,
            "year": 2020,
            "summary": self.book_1.summary,
            "isbn": self.book_1.isbn,
            "price": 340,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.book_1 =Book.objects.get(pk=self.book_1.pk)
        self.book_1.refresh_from_db()
        self.assertEqual(340, self.book_1.price)
        self.assertEqual("2020", self.book_1.year)

    def test_update_not_owner(self):
        url = reverse("book-detail", kwargs={"pk": self.book_1.pk})
        self.user_2 = get_user_model().objects.create(username="test_user_2")
        data = {
            "title": self.book_1.title,
            "year": 2020,
            "summary": self.book_1.summary,
            "isbn": self.book_1.isbn,
            "price": 340,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_2)
        response = self.client.put(url, json_data, content_type="application/json")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(159, self.book_1.price)
        self.assertEqual("2000", self.book_1.year)

    def test_update_not_owner_but_staff(self):
        url = reverse("book-detail", kwargs={"pk": self.book_1.pk})
        self.user_staff = get_user_model().objects.create(
            username="test_user_staff", is_staff=True
        )
        data = {
            "title": self.book_1.title,
            "year": 2020,
            "summary": self.book_1.summary,
            "isbn": self.book_1.isbn,
            "price": 340,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_staff)
        response = self.client.put(url, json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(340, self.book_1.price)
        self.assertEqual("2020", self.book_1.year)


class BooksRelationTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(username="test_user")
        self.user2 = get_user_model().objects.create(username="test_user2")
        self.book_1 = Book.objects.create(
            title="Book_1",
            year=2000,
            summary="Summary book_1",
            isbn=123456789,
            price=159,
            owner=self.user,
        )
        self.book_2 = Book.objects.create(
            title="Book_2",
            year=2001,
            summary="Summary book_2",
            isbn=123456789,
            price=159,
        )

    def test_like(self):
        url = reverse("userbookrelation-detail", kwargs={"book": self.book_1.pk})
        data = {
            "like": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.like)

        data = {
            "in_bookmarks": True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        url = reverse("userbookrelation-detail", kwargs={"book": self.book_1.pk})
        data = {
            "rate": 3,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertEqual(3, relation.rate)

    def test_rate_wrong(self):
        url = reverse("userbookrelation-detail", kwargs={"book": self.book_1.pk})
        data = {
            "rate": 6,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
