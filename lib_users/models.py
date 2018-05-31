import datetime
import logging

from django.db import models
from django.utils.functional import cached_property

logger = logging.getLogger(__name__)


class LibUsers(models.Model):
    name = models.CharField(max_length=100)
    uid = models.CharField(null=False, blank=False, max_length=100)

    def __str__(self):
        return 'User {uid} ({name})'.format(uid=self.uid, name=self.name)

    @classmethod
    def create_lib_user(cls, name, uid):
        cls(name=name, uid=uid).save()

    def lent(self, book, duration=0):
        """
        Lent a book for the user
        :param duration: duration of lent in days
        :param book: Book to lent for
        :return: None
        """
        duration *= 24*60
        if book.is_available:
            self.lent__set.add(lib_user=self, book=book, duration=duration)
        else:
            # todo 5/19/18 felixraj : Raise exception here
            logger.warning(msg="An exception occurred during creating lent")
            pass

    # todo 5/19/18 felixraj : Define exceptions to use with this class


class Lent(models.Model):
    DEFAULT_LENT_DURATION = 14

    lib_user = models.ForeignKey(LibUsers, on_delete=models.CASCADE)
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    lent_on = models.DateField(auto_now_add=True)
    duration = models.DurationField(default=DEFAULT_LENT_DURATION)

    class Meta:
        ordering = ('lib_user',)

    def __str__(self):
        return '{book} with {lib_user}'.format(
            book=self.book,
            lib_user=self.lib_user
        )

    def save(self, *args, **kwargs):
        if self.duration == 0:
            self.duration = datetime.timedelta(days=self.DEFAULT_LENT_DURATION)
        super(Lent, self).save(*args, **kwargs)

    @cached_property
    def due_on(self):
        return self.lent_on+self.duration