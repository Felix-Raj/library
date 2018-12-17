from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from lib_users.models import Lent


@receiver(post_save, model=Lent)
def lent_stock(sender, instance, created, **kwargs):
    print('lent out book')
    if not created:
        pass  # then edited ;-)
    else:
        print(instance)
        instance.book.lent_book()


@receiver(post_delete, model=Lent)
def return_stock(sender, instance, **kwargs):
    print('return book')
    print(instance)
    instance.book.return_book()
