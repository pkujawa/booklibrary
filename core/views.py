import requests
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, FormView, UpdateView
from django_filters import rest_framework
from rest_framework import generics

from .filters import BookAPIFilter, BookFilter
from .forms import SearchForm
from .models import Book
from .serializers import BookSerializer


def index(request):
    listofbooks = BookFilter(request.GET, queryset=Book.objects.all())

    return render(request, "core/bookdisplay.html", {"books": listofbooks})


class BookCreateView(CreateView):
    model = Book
    fields = [
        "title",
        "author",
        "language",
        "date_published",
        "ISBN_number",
        "page_number",
        "link_to_cover",
    ]


class BookUpdateView(UpdateView):
    model = Book
    fields = [
        "title",
        "author",
        "language",
        "date_published",
        "ISBN_number",
        "page_number",
        "link_to_cover",
    ]
    template_name_suffix = "_update_form"


class BookImport(FormView):
    template_name = "core/book_search.html"
    form_class = SearchForm
    success_url = "/core/"

    @staticmethod
    def get_url(form):
        lookup = {
            "intitle": form.data["title"],
            "inauthor": form.data["author"],
            "isbn": form.data["ISBN_number"],
        }
        lookupstring = "+".join([f"{k}:{v}" for k, v in lookup.items() if v])
        url = "https://www.googleapis.com/books/v1/volumes?q=" + lookupstring
        return url

    @staticmethod
    def get_full_date(datestring):
        """
        Google books API not always returns full date in publishedDate,
        that`s why its important to add missing months or/and days
        """
        date = datestring.split("-")
        if len(date) == 3:
            fulldate = datestring
        elif len(date) == 2:
            fulldate = datestring + "-01"
        else:
            fulldate = datestring[:4] + "-01-01"
        return fulldate

    @staticmethod
    def get_isbn_number(isbn):
        for number in isbn:
            if number["type"] == "ISBN_13":
                return number["identifier"]
        return None

    def form_valid(self, form):
        url = self.get_url(form)

        r = requests.get(url)
        json = r.json()
        for i in json["items"]:
            i = i["volumeInfo"]
            b = Book()
            b.title = i["title"]
            b.author = ", ".join(i["authors"])
            b.language = i["language"]

            b.date_published = self.get_full_date(i["publishedDate"])

            b.page_number = i.get("pageCount")
            b.ISBN_number = self.get_isbn_number(i["industryIdentifiers"])
            b.save()

        return redirect("index")


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = BookAPIFilter
