from django.db.models import Avg

from .models import Book, UserBookRelation


def set_rating(book: Book):
    raring = UserBookRelation.objects.filter(book=book).aggregate(rating=Avg("rate")).get("rating")
    book.rating = raring
    book.save()
