import logging

from django.contrib.postgres.fields import JSONField
from django.db import models

logger = logging.getLogger(__name__)


class Book(models.Model):
    MAGAZINE = 'magazine'
    COMICS = 'comics'
    BOOKS = 'books'
    EDUCATIONAL = 'educational'
    BOOK_CATEGORIES = (
        (MAGAZINE, MAGAZINE.capitalize()),
        (COMICS, COMICS.capitalize()),
        (EDUCATIONAL, EDUCATIONAL.capitalize()),
        (BOOKS, BOOKS.capitalize())
    )

    book_id = models.CharField(null=False, blank=False, max_length=100, default=0, unique=True)
    title = models.TextField()
    author = models.TextField()
    copies = models.IntegerField(default=1)
    notes = models.TextField()
    copies_on_lent = models.IntegerField(default=0)
    category = models.CharField(choices=BOOK_CATEGORIES, default=BOOKS, max_length=10)
    price = models.FloatField(default=0)
    locked = models.BooleanField(default=False)
    preview = JSONField(default={})

    def __str__(self):
        return '{book} by {author}'.format(book=self.title, author=self.author)

    def add_tag(self, tag_list):
        tag_list = filter(lambda tag: not self.has_tag(tag), tag_list)
        for tag in tag_list:
            BookTag(book=self, tag=tag.strip().lower()).save()

    def has_tag(self, tag):
        return self.booktag_set.all().filter(tag__iexact=tag.lower()).count() > 0

    def _toggle_lock_state(self):
        self.locked = not self.locked
        self.save()

    def lock(self):
        if not self.locked:
            self._toggle_lock_state()

    def unlock(self):
        if self.locked:
            self._toggle_lock_state()

    def return_book(self, count=1):
        self.copies_on_lent -= count
        self.save()

    def lent_book(self, count=1):
        """
        Increases the copies_on_lent by one, only if book is available to lent.

        :param count: count of book to lent out
        :return:
        """
        if self.is_available:
            self.copies_on_lent += count
            self.save()
        else:
            logger.warning(msg='Book Not available')

    @property
    def is_available(self):
        return not self.locked and (self.copies > self.copies_on_lent)


class BookTag(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100)
