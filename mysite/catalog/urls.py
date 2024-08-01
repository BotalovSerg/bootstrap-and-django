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
    path("edit_authors/", views.list_edit_authors, name="edit-authors-list"),
    path("add_author/", views.add_author, name="author-add"),
    path("edit_author/<int:pk>/", views.edit_author, name="edit-author"),
    path("delete_author/<int:pk>/", views.delete_author, name="del-author"),

    path("edit_books/", views.edit_books, name="edit_books"),
    path("book_create/", views.BookCreate.as_view(), name="book_create"),
    path("book_update/<int:pk>/", views.BookUpdate.as_view(), name="book_update"),
    path("book_delete/<int:pk>/", views.BookDelete.as_view(), name="book_delete"),
]
