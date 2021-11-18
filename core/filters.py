import django_filters
from django_filters import rest_framework

from .models import Book


class BookAPIFilter(rest_framework.FilterSet):
    min_date = rest_framework.DateFilter(field_name="date_published", lookup_expr="gte")
    max_date = rest_framework.DateFilter(field_name="date_published", lookup_expr="lte")

    class Meta:
        model = Book
        fields = ["title", "author", "language", "min_date", "max_date"]


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            "title": ["icontains"],
            "author": ["icontains"],
            "language": ["icontains"],
            "date_published": ["year__gte", "year__lte"],
        }
