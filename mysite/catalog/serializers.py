from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Book, UserBookRelation


class BookReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name")


class BookSerializer(serializers.ModelSerializer):
    # likes_count = SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(
        source="owner.username",
        default="",
        read_only=True,
    )
    readers = BookReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "year",
            "summary",
            "isbn",
            "price",
            "annotated_likes",
            "rating",
            "owner_name",
            "readers",
        )

    # def get_likes_count(self, instance):
    # return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ("book", "like", "in_bookmarks", "rate")
