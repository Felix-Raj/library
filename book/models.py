from django.db import models


class Book(models.Model):
    book_id = models.CharField(null=False, blank=False, max_length=100, default=0)
    # todo 7/16/18 felixraj : mark book id as unique
    title = models.TextField()
    author = models.TextField()
    copies = models.IntegerField(default=1)
    notes = models.TextField()

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
