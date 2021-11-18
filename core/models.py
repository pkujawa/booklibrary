from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    date_published = models.DateField()
    ISBN_number = models.CharField(
        max_length=13, validators=[MinLengthValidator(13)], null=True
    )
    page_number = models.PositiveIntegerField(null=True)
    link_to_cover = models.URLField(max_length=200, null=True)
    language = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse("index")

    def __str__(self):
        return f"Title: {self.title}"
