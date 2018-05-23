from django.db import models


class Book(models.Model):
    title = models.TextField()
    author = models.TextField()
    copies = models.IntegerField(default=1)

    def __str__(self):
        return '{book} by {author}'.format(book=self.title, author=self.author)

    def add_tag(self, tag_list):
        tag_list = filter(lambda tag: not self.has_tag(tag), tag_list)
        for tag in tag_list:
            BookTag(book=self, tag=tag.strip().lower()).save()

    def has_tag(self, tag):
        return self.booktag_set.all().filter(tag__iexact=tag.lower()).count() > 0

    @property
    def is_available(self):
        # todo 5/19/18 felixraj : complete this function
        return False


class BookTag(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100)
