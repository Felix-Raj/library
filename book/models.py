from django.db import models


class Book(models.Model):
    title = models.TextField()
    author = models.TextField()

    def __str__(self):
        return '{book} by {author}'.format(book=self.title, author=self.author)


class BookTag(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100)
