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
    USER_CHOICES=(
        (STUDENT, STUDENT.upper()),
        (TEACHER, TEACHER.upper()),
        (DEFAULT, DEFAULT.upper()),
    )

    name = models.CharField(max_length=100)
    uid = models.CharField(null=False, blank=False, max_length=100)
    avatar = JSONField(default={}, null=True)
    user_type = models.CharField(choices=USER_CHOICES, default=DEFAULT, max_length=100)
    account_activated = models.BooleanField(default=False)
    date_of_birth = models.DateField(default=datetime.datetime.today)
    # todo 8/8/18 felixraj : change blank,null = True
    father = models.CharField(max_length=100, blank=True, null=True)
    mother = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering=('name',)

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

    def _toggle_activation_state(self):
        """
        Toggle the activation state of a user account
        """
        self.account_activated = not self.account_activated
        self.save()

    def activate_account(self):
        """
        Helper function to activate account
        """
        if not self.account_activated:
            self._toggle_activation_state()

    def de_activate_account(self):
        """
        Helper to deactivate account.
        """
        if self.account_activated:
            self._toggle_activation_state()

    @staticmethod
    def can_lent(libuser):
        """
        Return True if this user can lent books.

        :param libuser: user for which the check is made
        :return: True or raises ValidationError

        :raises ValidationError: if any condition is not satisfied
        """
        test_to_perform = [
            (libuser.account_activated, 'Account not activated'),
            # (Result of test function, 'Error message')
        ]
        errors = list()
        for test, error_message in test_to_perform:
            if not test:
                errors.append(error_message)
        if errors:
            raise ValidationError(message=errors)
        return True
    # todo 5/19/18 felixraj : Define exceptions to use with this class


def book_available(book):
    if book.is_available:
        return True
    else:
        raise ValidationError(message='Book not available')


class Lent(models.Model):
    DEFAULT_LENT_DURATION = 14

    lib_user = models.ForeignKey(LibUsers, on_delete=models.CASCADE, validators=[LibUsers.can_lent])
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