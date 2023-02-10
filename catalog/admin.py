from django.contrib import admin

from .models import Author, Book, BookCopy, Genre, Language

admin.register(Author)
admin.register(Book)
admin.register(BookCopy)
admin.register(Genre)
admin.register(Language)
