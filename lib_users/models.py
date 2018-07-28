import datetime
import logging

from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property

logger = logging.getLogger(__name__)


class LibUsers(models.Model):
    STUDENT = 'student'
    TEACHER = 'teacher'
    DEFAULT = 'default'

    name = models.CharField(max_length=100)
    uid = models.CharField(null=False, blank=False, max_length=100)
    avatar = JSONField()
    user_type = models.CharField(
        choices=(
            (STUDENT, STUDENT.upper()),
            (TEACHER, TEACHER.upper()),
            (DEFAULT, DEFAULT.upper()),
        ),
        default=DEFAULT,
        max_length=100
    )
    date_of_birth = models.DateField(default=datetime.datetime.today)

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

    def lent_status(self):
        """
        Find weather the user had already lent some books. Then returns a queryset
        containing the books lent
        """
        return self.lent_set.all()
    # todo 5/19/18 felixraj : Define exceptions to use with this class


def book_available(book):
    if book.is_available:
        return True
    else:
        raise ValidationError(message='Book not available')


class Lent(models.Model):
    DEFAULT_LENT_DURATION = 14

    lib_user = models.ForeignKey(LibUsers, on_delete=models.CASCADE)
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE, validators=[book_available])
    lent_on = models.DateField(auto_now_add=True)
    duration = models.DurationField(default=DEFAULT_LENT_DURATION)

    class Meta:
        ordering = ('lent_on',)

    def __str__(self):
        return '{book} with {lib_user}'.format(
            book=self.book,
            lib_user=self.lib_user
        )

    def save(self, *args, **kwargs):
        if self.duration == datetime.timedelta(days=0):
            self.duration = datetime.timedelta(days=self.DEFAULT_LENT_DURATION)

        self.book.lent_book()
        super(Lent, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.book.return_book()
        super(Lent, self).delete(using, keep_parents)

    @cached_property
    def due_on(self):
        return self.lent_on+self.duration