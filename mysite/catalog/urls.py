from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("accounts/logout/", views.logout_view, name="logout"),

    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("authors/", views.AuthorListView.as_view(), name="authors-list"),
    path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="authors-detail"),
    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    path("edit_authors/", views.edit_authors, name="edit-authors-list"),
    path("add_author/", views.add_author, name="author-add"),
    path("edit_authors/<int:pk>/", views.edit_authors, name="edit-author"),
    path("del/<int:pk>/", views.edit_authors, name="del-author"),
]
