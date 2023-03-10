import uuid

from django.db import models
from django.shortcuts import reverse


class Author(models.Model):
    """A model representing a book Author."""
    name = models.CharField(
        null=False, blank=False, max_length=64,
        help_text='Enter the name of the book author.')

    def __str__(self):
        """String representing the authors."""
        return self.name


class Categories(models.Model):
    """A model representing a book genre."""
    UNKNOWN = 'Unknown'
    name = models.CharField(
        null=False, blank=False, max_length=64,
        help_text='Enter the name of the genre '
                  '(e.g. fiction, historical, etc..).')

    def __str__(self):
        """String representing the genre."""
        return self.name


class Book(models.Model):
    """A model representing the general information of a book."""
    isbn = models.CharField(
        'ISBN', max_length=13,
        help_text='Enter the book\'s 13 digit ISBN.'
                  'see <a href="'
                  'https://www.isbn-international.org/content/what-isbn'
                  '">ISBN number</a> for details.')
    title = models.CharField(
        max_length=256, blank=False, null=False,
        help_text='Enter the book\'s title.')
    subtitle = models.CharField(
        max_length=256, blank=True, null=True,
        help_text='Enter the book\'s subtitle,'
                  'can be left empty.')
    authors = models.ManyToManyField(
        Author, through='BooksAuthors',
        help_text='Choose the book\'s author/s.')
    publication_year = models.PositiveSmallIntegerField(
        blank=False, null=False,
        help_text='Enter the year of the book\'s publication.')
    categories = models.ForeignKey(
        Categories, on_delete=models.RESTRICT,
        blank=False, null=False,
        help_text='Choose the genres to which the book belongs.')
    thumbnail = models.URLField(
        max_length=256, blank=True, null=True,
        help_text='Enter a url for the books thumbnail picture,'
                  'can be left blank.')
    summary = models.TextField(
        max_length=1024, blank=True, null=True,
        help_text='Enter a short summary of the book,'
                  'can be left empty.')
    page_count = models.PositiveSmallIntegerField(
        blank=False, null=False, default=0,
        help_text='Enter the number of pages in the book.')
    average_rating = models.DecimalField(
        max_digits=4, decimal_places=2,
        blank=False, null=False, default=5,
        help_text='Enter a previously known user rating,'
                  'can be left blank.')
    ratings_count = models.PositiveIntegerField(
        blank=False, null=False, default=0,
        help_text='Enter a previously known count of user ratings,'
                  'can be left blank.')

    class Meta:
        pass
        # ordering = ['title', 'authors', 'genre', 'ISBN', 'summary']

    def get_absolute_url(self):
        """Return the URL to access the general details of the book."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String representing the book's general information."""
        return f'{self.title}'
        # match self.authors:
        #     case []:
        #         authors_string = 'authors unknown'
        #     case [single_author]:
        #         authors_string = str(single_author)
        #     case [author_1, author_2]:
        #         authors_string = str(author_1) + ' and ' + str(author_2)
        #     case [*multiple_authors]:
        #         authors_string = ', '.join(
        #             str(author) for author in multiple_authors[:-1])
        #         authors_string = (authors_string + ' and '
        #                           + str(multiple_authors[-1]))
        #     case _:
        #         raise Exception('Unexpected error while trying to generate '
        #                         '__str__ for Book instance.')
        # return f'{self.title} by {authors_string}'

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.title}'


class BooksAuthors(models.Model):
    """Auxiliary relation Books-Authors model.

    This model is in place to prevent authors from being deleted
    if they there are books referencing them.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT)


class BookCopy(models.Model):
    """A model representing a single loanable copy of a book."""
    class LoanStatus(models.TextChoices):
        """An enum representing wherever a book instance's availability."""
        AVAILABLE = 'A'
        ON_LOAN = 'L'
        RESERVED = 'R'
        MAINTENANCE = 'M'

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        help_text='A unique id for the book copy across the whole library.')
    book = models.ForeignKey(
        Book, on_delete=models.RESTRICT,
        help_text='Choose the book copy\'s general information entry.')
    due_back = models.DateField(
        blank=True, null=True,
        help_text='Enter the date by which the book should be returned '
                  'if it\'s on loan,'
                  ' leave blank if the book is not currently on loan.')
    status = models.CharField(
        max_length=1, null=False, blank=True,
        choices=LoanStatus.choices, default=LoanStatus.MAINTENANCE,
        help_text='Book Availability')
    borrower = 'To be implemented'

    # borrower = models.ForeignKey(
    #     User, blank=True, null=True, on_delete=models.DO_NOTHING,
    #     help_text='Enter the library user currently borrowing the book,'
    #               ' leave blank if the book is not currently on loan.')

    class Meta:
        pass
        # ordering = ['id', 'book', 'imprint', 'status', 'due_back']

    def get_absolute_url(self):
        """Return the URL for the book copy's details."""
        return reverse('book_copy-details', args=[str(self.id)])

    def __str__(self):
        """ String representing the book copy's loan status and information."""
        match self.status:
            case self.LoanStatus.AVAILABLE:
                status = 'Available'
            case self.LoanStatus.ON_LOAN:
                status = (f'On loan to {self.borrower!s},'
                          f' due back on {self.due_back!s}')
            case self.LoanStatus.RESERVED:
                status = f'Reserved by {self.borrower!s}'
            case self.LoanStatus.MAINTENANCE:
                status = (f'undergoing maintenance {self.borrower!s},'
                          f' due back on {self.due_back!s}')
            case _:
                status = 'This status should never happen.'
        return (
            f'{self.book!s}. {status}.'
        )
