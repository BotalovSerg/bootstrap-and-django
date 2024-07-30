from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    Book,
    Author,
    Genre,
    Language,
    Publisher,
    Status,
    BookInstance,
)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "photo", "show_photo"]
    fields = ["last_name", "first_name", "about", ("date_of_birth", "photo")]

    @admin.display(description="Фото")
    def show_photo(self, obj: Author):
        return format_html(f"<img src='{obj.photo.url}' style='max-height: 100px;'>")


class BookInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "genre", "language", "display_author", "show_photo"]
    list_filter = ["genre", "author"]
    inlines = [BookInstanceInline]

    @admin.display(description="Обложка")
    def show_photo(self, obj: Book):
        return format_html(f"<img src='{obj.photo.url}' style='max-height: 100px;'>")


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ["book", "status", "borrower", "due_back", "id"]
    list_filter = ["book", "status"]
    fieldsets = (
        (
            "Экземпляр книги",
            {
                "fields": ("book", "inv_num"),
            },
        ),
        (
            "Статус и окончание его действия",
            {
                "fields": ("status", "due_back", "borrower"),
            },
        ),
    )


admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Publisher)
admin.site.register(Status)
