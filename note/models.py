from django.db import models


class Note(models.Model):
    note = models.TextField()

    class Meta:
        ordering = ('-id',)