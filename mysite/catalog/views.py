from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    text_head = "Это заголовк главной страницы"
    text_body = "This is content main page"
    context = {"text_head": text_head, "text_body": text_body}
    return render(request, "catalog/index.html", context=context)
