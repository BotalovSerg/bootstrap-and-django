from datetime import date

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Введите жанр книги",
        verbose_name="Жанр книги",
    )

    def __str__(self) -> str:
        return self.name


class Language(models.Model):
    name = models.CharField(
        max_length=20,
        help_text="Введите язык книги",
        verbose_name="Язык книги",
    )

    def __str__(self) -> str:
        return self.name


class Publisher(models.Model):
    name = models.CharField(
        max_length=20,
        help_text="Введите наименование издательства",
        verbose_name="Издательство",
    )

    def __str__(self) -> str:
        return self.name


class Author(models.Model):
    first_name = models.CharField(
        max_length=100,
        help_text="Введите имя автора",
        verbose_name="Имя автора",
    )
    last_name = models.CharField(
        max_length=100,
        help_text="Введите фамилию автора",
        verbose_name="Фамилия автора",
    )
    date_of_birth = models.DateField(
        help_text="Введите дату рождения",
        verbose_name="Дата рождения",
        null=True,
        blank=True,
    )
    about = models.TextField(
        help_text="Введите сведения об авторе",
        verbose_name="Сведения об авторе",
    )
    photo = models.ImageField(
        upload_to="images",
        help_text="Загрузите фото автора",
        verbose_name="Фото автора",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.last_name


class Book(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Введите название книги",
        verbose_name="Название книги",
    )
    genre = models.ForeignKey(
        "Genre",
        on_delete=models.CASCADE,
        null=True,
        help_text="Выберите жанр книги",
        verbose_name="Жанр книги",
        blank=True,
    )
    language = models.ForeignKey(
        "Language",
        on_delete=models.CASCADE,
        null=True,
        help_text="Выберите язык книги",
        verbose_name="Язык книги",
        blank=True,
    )
    publisher = models.ForeignKey(
        "Publisher",
        on_delete=models.CASCADE,
        null=True,
        help_text="Выберите издательство",
        verbose_name="Издательство",
        blank=True,
    )
    year = models.CharField(
        max_length=4,
        help_text="Введите год издания",
        verbose_name="Год издания",
    )
    author = models.ManyToManyField(
        "Author",
        help_text="Выберите автора (авторов) книги",
        verbose_name="Автор (авторы) книги",
    )
    summary = models.TextField(
        max_length=1000,
        help_text="Введите краткое описание книги",
        verbose_name="Аннотация книги",
        blank=True,
    )
    isbn = models.CharField(
        max_length=13,
        help_text="Должно содержать 13 символов",
        verbose_name="ISBN книги",
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=7,
        help_text="Введите цену книги",
        verbose_name="Цена (руб.)",
    )
    photo = models.ImageField(
        upload_to="images",
        help_text="Загрузите изображение обложки",
        verbose_name="Изображение обложки",
        blank=True,
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="my_books",
    )

    readers = models.ManyToManyField(
        get_user_model(), through="UserBookRelation", related_name="read_books"
    )

    rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=None, null=True
    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        # return reverse("book-detail", args=[str(self.id)])
        return reverse("book-detail", kwargs={"pk": self.pk})

    def display_author(self):
        return ", ".join([author.last_name for author in self.author.all()])

    display_author.short_description = "Авторы"


class Status(models.Model):
    name = models.CharField(
        max_length=20,
        help_text="Введите статус экземпляра книги",
        verbose_name="Статус экземпляра книги",
    )

    def __str__(self) -> str:
        return self.name


class BookInstance(models.Model):

    class Meta:
        ordering = ["due_back"]

    book = models.ForeignKey(
        "Book",
        on_delete=models.CASCADE,
        null=True,
    )
    inv_num = models.CharField(
        max_length=20,
        help_text="Введите инвентарный номер экземпляра",
        verbose_name="Инвентарный номер",
    )
    status = models.ForeignKey(
        "Status",
        on_delete=models.CASCADE,
        null=True,
        help_text="Изменить состояние экзампляра",
        verbose_name="Статус экзампляра книги",
    )
    due_back = models.DateField(
        null=True,
        help_text="Введите конец срока статуса",
        verbose_name="Дата окончания статуса",
    )
    borrower = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Заказчик",
        help_text="Веберите заказчика книги",
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self) -> str:
        return f"{self.inv_num} {self.book} {self.status}"


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, "OK"),
        (2, "Fine"),
        (3, "Good"),
        (4, "Amazing"),
        (5, "Incredebl"),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self) -> str:
        return f"{self.user.username}: {self.book!r} rate -> {self.rate}"

    def save(self, *args, **kwargs) -> None:
        from .loginc import set_rating

        creating = not self.pk
        old_rating = self.rate
        super().save(*args, **kwargs)
        new_raring = self.rate
        if old_rating != new_raring or creating:
            set_rating(self.book)
