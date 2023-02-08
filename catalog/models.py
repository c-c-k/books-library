import enum
import uuid

from django.db import models
from django.shortcuts import reverse


class LoanStatus(enum.IntEnum):
    """An enum representing wherever a book instance's availability."""
    AVAILABLE = enum.auto()
    ON_LOAN = enum.auto()
    RESERVED = enum.auto()
    MAINTENANCE = enum.auto()

    @staticmethod
    def selection_map():
        return tuple((str(status.value), str(status.name).title().replace('_', ' '))
                     for status in LoanStatus)


class User:
    """Placeholder until a proper user is defined."""
    pass


class Author(models.Model):
    """A model representing a book Author."""
    name = models.CharField(max_length=64,
                            help_text='Enter the name of the book author.')
    date_of_birth = models.DateField(
        blank=True, null=True,
        help_text='Enter the date of the book authors birth,'
                  ' leave blank if unknown.')
    date_of_death = models.DateField(
        blank=True, null=True,
        help_text='Enter the date of the book authors death,'
                  ' leave blank if unknown or if author is still alive.')

    class Meta:
        ordering = ['name', 'date_of_birth', 'date_of_birth']

    def __str__(self):
        """String representing the author."""
        return self.name


class Genre(models.Model):
    """A model representing a book genre."""
    name = models.CharField(max_length=32,
                            help_text='Enter the name of the genre (e.g. '
                                      'fiction, historical, etc..).')

    class Meta:
        ordering = ['name']

    def __str__(self):
        """String representing the genre."""
        return self.name


class Language(models.Model):
    """A model representing a book genre."""
    name = models.CharField(max_length=32,
                            help_text='Enter the name of the language (e.g.'
                                      'english, french, etc..).')

    class Meta:
        ordering = ['name']

    def __str__(self):
        """String representing the language."""
        return self.name


class Book(models.Model):
    """A model representing the general information of a book."""
    title = models.CharField(max_length=256, help_text='Enter the book\'s title.')
    author = models.ForeignKey(Author, on_delete=models.RESTRICT,
                               help_text='Choose the book\'s author.')
    summary = models.TextField(max_length=1024, blank=True, null=True,
                               help_text='Enter a short summary of the book,'
                                         'can be left empty.')
    ISBN = models.CharField('ISBN', max_length=13, unique=True,
                            help_text='Enter the book\'s ISBN.'
                                      'see <a href="https://www.'
                                      'isbn-international.org/content/'
                                      'what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre,
                                   help_text='Choose the genres to which the book belongs.')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True,
                                 help_text='Choose the book\'s language.')

    class Meta:
        ordering = ['title', 'author', 'language', 'genre', 'ISBN', 'summary']

    def get_absolute_url(self):
        """Return the URL to access the general details of the book."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String representing the book's general information."""
        return (
            f'{self.title} by {self.author!s},'
            f' language: {self.language!s}, ISBN: {self.ISBN}'
        )


class BookCopy(models.Model):
    """A model representing a single loanable copy of a book."""
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        help_text='A unique id for the book copy across the whole library.')
    book = models.ForeignKey(
        Book, on_delete=models.RESTRICT,
        help_text='Choose the book copy\'s general information entry.')
    imprint = models.CharField(
        max_length=264, help_text='Enter the books copy\'s imprint '
                                  '(specific release/version info).')
    due_back = models.DateField(
        blank=True, null=True,
        help_text='Enter the date by which the book should be returned '
                  'if it\'s on loan,'
                  ' leave blank if the book is not currently on loan.')
    status = models.SmallIntegerField(
        null=False, blank=True, default=LoanStatus.MAINTENANCE.value,
        choices=LoanStatus.selection_map(),
        help_text='Book Availability')
    borrower = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.DO_NOTHING,
        help_text='Enter the library user currently borrowing the book,'
                  ' leave blank if the book is not currently on loan.')

    class Meta:
        ordering = ['unique_id', 'book', 'imprint', 'status', 'due_back', 'borrower']

    def get_absolute_url(self):
        """Return the URL for the book copy's details."""
        return reverse('book_copy-details', args=[str(self.id)])

    def __str__(self):
        """String representing the book copy's loan status and general information."""
        match self.status:
            case LoanStatus.AVAILABLE:
                status = 'Available'
            case LoanStatus.ON_LOAN:
                status = (f'On loan to {self.borrower!s},'
                          f' due back on {self.due_back!s}')
            case LoanStatus.RESERVED:
                status = f'Reserved by {self.borrower!s}'
            case LoanStatus.MAINTENANCE:
                status = (f'undergoing maintenance {self.borrower!s},'
                          f' due back on {self.due_back!s}')
            case _:
                status = 'This status should never happen.'
        return (
            f'{self.book!s}. {status}.'
        )
