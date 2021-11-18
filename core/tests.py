from unittest.mock import patch

import pytest

from .models import Book
from .views import BookImport


class FormClass:
    def __init__(self, data):
        self.data = data


class TestBookImportGetUrl:
    def test_get_url_3_filters(self):

        form = FormClass(
            {
                "title": "Test Title",
                "author": "Test author",
                "ISBN_number": "Test ISBN",
            }
        )
        book_import = BookImport()
        url = book_import.get_url(form)
        assert (
            url == "https://www.googleapis.com/books/v1/volumes?q="
            "intitle:Test Title+inauthor:Test author+isbn:Test ISBN"
        )

    def test_get_url_without_title(self):
        form = FormClass(
            {
                "title": "",
                "author": "Test author",
                "ISBN_number": "Test ISBN",
            }
        )
        book_import = BookImport()
        url = book_import.get_url(form)
        assert (
            url == "https://www.googleapis.com/books/v1/volumes?q="
            "inauthor:Test author+isbn:Test ISBN"
        )


class TestBookImportGetFullDate:
    @pytest.mark.parametrize(
        "input_date, output_date",
        [
            ("2020-10-10", "2020-10-10"),
            ("2020-10", "2020-10-01"),
            ("2020", "2020-01-01"),
            ("2020*", "2020-01-01"),
        ],
    )
    def test_get_full_date_full_date(self, input_date, output_date):
        book_import = BookImport()
        full_date = book_import.get_full_date(input_date)
        assert full_date == output_date


class TestBookImportGetISBNNumber:
    def test_get_isbn_number(self):
        test_data = [
            {"type": "ISBN_10", "identifier": 1234567890},
            {"type": "ISBN_13", "identifier": 1234567890123},
        ]

        book_import = BookImport()
        isbn = book_import.get_isbn_number(test_data)
        assert isbn == 1234567890123


class TestBookImportFormValid:
    class MockRequest:
        def __init__(self, data):
            self.data = data

        def json(self):
            return self.data

    @pytest.mark.django_db
    def test_form_valid(self):
        with patch("requests.get") as requests_get:
            data = {
                "items": [
                    {
                        "volumeInfo": {
                            "title": "Title",
                            "authors": ["A. U. Thor", "S Econd"],
                            "language": "eng",
                            "publishedDate": "2020-10",
                            "pageCount": 100,
                            "industryIdentifiers": [
                                {
                                    "type": "ISBN_10",
                                    "identifier": 1234567890,
                                },
                                {
                                    "type": "ISBN_13",
                                    "identifier": 1234567890123,
                                },
                            ],
                        },
                    },
                ],
            }
            requests_get.return_value = self.MockRequest(data)
            book_import = BookImport()
            form = FormClass(
                {
                    "title": "Test Title",
                    "author": "Test author",
                    "ISBN_number": "Test ISBN",
                }
            )
            book_import.form_valid(form)
            assert Book.objects.count() == 1
