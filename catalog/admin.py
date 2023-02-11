from django.contrib import admin

from .models import Author, Book, BookCopy, Categories

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Categories)
