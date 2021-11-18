from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.BookCreateView.as_view(), name="bookadd"),
    path("<pk>/update", views.BookUpdateView.as_view(), name="bookupdate"),
    path("search", views.BookImport.as_view(), name="bookimport"),
    path("api/", views.BookList.as_view(), name="api-list"),
]
