import csv
# import datetime
from decimal import Decimal
# from itertools import islice
from pathlib import Path
from pprint import pprint
# from random import randint

# from django.db.models import Model

from ..models import Author, Categories, Book  # , BookCopy

DATASET_ROOT = Path(__file__).parent / 'datasets/'
DATASET_7K_BOOKS = DATASET_ROOT / 'books_7k.csv'


def get_sample_entry_from_csv(csv_file: Path, print_=False, temp_file=True):
    """Get a sample entry to use as reference while writing importer code.

    :param csv_file: The csv file to get the reference from.
    :param print_: Set to True to output the sample to the console.
    :param temp_file: Set to False in order to avoid creating a sample file.
    :return: None.
    """
    with open(csv_file, 'r', newline='') as csv_io:
        csv_dict = csv.DictReader(csv_io)
        sample_entry = next(csv_dict)
    if print_:
        pprint(sample_entry)
        pprint(sample_entry.keys(), width=50)
    if temp_file:
        with open(DATASET_ROOT / '_sample_entry.tmp', 'w') as sample_file:
            pprint(sample_entry, stream=sample_file)
            print(f'Exported to {sample_file.name}')


def get_field_values_from_csv(
        csv_file: Path, field_name: str, sub_list_sep: str | None = None,
        print_=False, temp_file=True, return_values=False
) -> set | None:
    """Get all values for a field to use as reference while writing importer
    code.

    :param sub_list_sep: A separator string to split lists appearing within
        a single field into separate values, if left as None the sub lists
        are left as they are.
    :param return_values: Return values to caller.
    :param csv_file: The csv file to get the reference from.
    :param field_name: The name of the field for which to get the values.
    :param print_: Set to True to output the sample to the console.
    :param temp_file: Set to False in order to avoid creating a sample file.
    :return: values if return_values is true else None
    """
    with open(csv_file, 'r', newline='') as csv_dataset:
        csv_dict = csv.DictReader(csv_dataset)
        values = set(csv_entry[field_name] for csv_entry in csv_dict)
    if sub_list_sep:
        sub_list_values = values
        values = set()
        for sub_list_value in sub_list_values:
            values.update(sub_list_value.split(sub_list_sep))
    values = sorted(values)
    if print_:
        pprint(values, width=50)
    if temp_file:
        temp_file_path = DATASET_ROOT / f'_values_{field_name}.tmp'
        with open(temp_file_path, 'w') as sample_file:
            print(*values, file=sample_file, sep='\n')
            print(f'Exported to {sample_file.name}')
    return values if return_values else None


def import_7k_books():
    """Import books from a 7k books dataset csv.

    7k dataset Attributions:
        * Author : DylanCastillo
        * Link : Kaggle_

        .. _Kaggle:
            https://www.kaggle.com/ datasets/
            dylanjcastillo/7k-books-with-metadata
    """

    def clear_prev_data():
        Book.objects.all().delete()
        Author.objects.all().delete()
        Categories.objects.all().delete()

    #
    # def bulk_import(model, names):
    #     batch_size = 1000
    #     while True:
    #         batch = islice(names, batch_size)
    #         if not batch:
    #             break
    #         model.objects.bulk_create(batch, batch_size=batch_size)
    #
    # def import_categories():
    #     categories_names = get_field_values_from_csv(
    #         csv_file=DATASET_7K_BOOKS, field_name='categories',
    #         sub_list_sep=';', temp_file=False, return_values=True)
    #     bulk_import(Categories, categories_names)

    def books_data_from_dataset() -> dict:
        with open(DATASET_7K_BOOKS, 'r', newline='') as data_source:
            csv_dict_reader = csv.DictReader(data_source)
            yield from csv_dict_reader

    def create_book_from_dataset_data(_book_data_from_dataset: dict) -> Book:
        categories_name = (
            _book_data_from_dataset['categories']
            if _book_data_from_dataset['categories']
            else Categories.UNKNOWN
        )
        try:
            page_count = int(_book_data_from_dataset['num_pages'])
        except ValueError:
            page_count = 0
        return Book(
            isbn=_book_data_from_dataset['isbn13'],
            title=_book_data_from_dataset['title'],
            subtitle=_book_data_from_dataset['subtitle'],
            publication_year=int(_book_data_from_dataset['published_year']),
            categories=Categories.objects.get_or_create(
                name=categories_name)[0],
            thumbnail=_book_data_from_dataset['thumbnail'],
            summary=_book_data_from_dataset['description'],
            page_count=page_count,
            average_rating=Decimal(_book_data_from_dataset['average_rating']),
            ratings_count=int(_book_data_from_dataset['ratings_count']),
        )

    def set_authors(_book: Book, _book_data_from_dataset: dict):
        author_names = (
            author_name.strip()
            for author_name
            in _book_data_from_dataset['authors'].split(';')
        )
        authors_list = list(
            Author.objects.get_or_create(name=author_name)[0].id
            for author_name
            in author_names
        )
        _book.authors.add(*authors_list, through_defaults=None)

    entry_limit = 1000
    entry_count = 0
    clear_prev_data()
    for book_data_from_dataset in books_data_from_dataset():
        if entry_count > entry_limit:
            break
        entry_count += 1
        if (entry_count % (entry_limit / 10)) == 0:
            print(f'{entry_count}/{entry_limit} done.')
        book = create_book_from_dataset_data(book_data_from_dataset)
        book.save()
        set_authors(book, book_data_from_dataset)
