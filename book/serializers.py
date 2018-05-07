from rest_framework import serializers

from book.models import Book, BookTag


class BookTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTag
        fields = ('tag',)


class BookSerializer(serializers.ModelSerializer):
    booktag_set = BookTagSerializer(many=True)

    class Meta:
        model = Book
        fields = ('title', 'author', 'booktag_set')