from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "date_published",
            "ISBN_number",
            "page_number",
            "link_to_cover",
            "language",
        ]
