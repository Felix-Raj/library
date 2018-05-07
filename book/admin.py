from django.contrib import admin

from book.models import Book, BookTag


class BookTagInlineAdmin(admin.StackedInline):
    model = BookTag


class BookAdmin(admin.ModelAdmin):
    list_display = ('pk','title', 'author')
    list_filter = ('author','booktag__tag')
    inlines = [
        BookTagInlineAdmin
    ]


admin.site.register(Book, BookAdmin)
