from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

from .models import Book, Author, BookInstance


def index(request: HttpRequest) -> HttpResponse:
    text_head = "На нашем сайте вы можете получить книги в электронном виде"
    books = Book.objects.all()
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact=2).count()
    authors = Author.objects.all()
    num_authors = Author.objects.all().count()

    context = {
        "text_head": text_head,
        "books": books,
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "authors": authors,
        "num_authors": num_authors,
    }
    return render(request, "catalog/index.html", context=context)


class BookListView(ListView):
    model = Book
    context_object_name = "books"