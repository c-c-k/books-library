import csv
import datetime
from decimal import Decimal
from pathlib import Path
from pprint import pprint
from random import randint

from ..models import Author, Categories, Book, BookCopy

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
        csv_file: Path, field_name: str, print_=False, temp_file=True):
    """Get all values for a field to use as reference while writing importer
    code.

    :param csv_file: The csv file to get the reference from.
    :param field_name: The name of the field for which to get the values.
    :param print_: Set to True to output the sample to the console.
    :param temp_file: Set to False in order to avoid creating a sample file.
    :return: None.
    """
    with open(csv_file, 'r', newline='') as csv_dataset:
        csv_dict = csv.DictReader(csv_dataset)
        values = sorted(set(csv_entry[field_name] for csv_entry in csv_dict))
    if print_:
        pprint(values, width=50)
    if temp_file:
        temp_file_path = DATASET_ROOT / f'_values_{field_name}.tmp'
        with open(temp_file_path, 'w') as sample_file:
            print(*values, file=sample_file, sep='\n')
            print(f'Exported to {sample_file.name}')



def import_7k_books():
    """Import books from a 7k books dataset csv.

    7k dataset Attributions:
        * Author : DylanCastillo
        * Link : Kaggle_

        .. _Kaggle:
            https://www.kaggle.com/ datasets/
            dylanjcastillo/7k-books-with-metadata
    """

    def books_data_from_dataset() -> dict:
        with open(DATASET_7K_BOOKS, 'r', newline='') as data_source:
            csv_dict_reader = csv.DictReader(data_source)
            yield from csv_dict_reader

    def create_book_from_dataset_data(_book_data_from_dataset: dict) -> Book:
        return Book(
            isbn=_book_data_from_dataset['isbn13'],
            title=_book_data_from_dataset['title'],
            subtitle=_book_data_from_dataset['subtitle'],
            publication_year=int(_book_data_from_dataset['publication_year']),
            thumbnail=_book_data_from_dataset['thumbnail'],
            summary=_book_data_from_dataset['summary'],
            page_count=int(_book_data_from_dataset['page_count']),
            average_rating=Decimal(_book_data_from_dataset['average_rating']),
            ratings_count=int(_book_data_from_dataset['ratings_count']),
        )

    for book_data_from_dataset in books_data_from_dataset():
        book = create_book_from_dataset_data(book_data_from_dataset)

    def is_invalid_entry(entry: dict):
        name = entry['name']
        return (',' in name) or (';' in name)

    def filter_book_entry(source_entry_: dict) -> dict:
        return {
            'name': source_entry_['bibliography.title'],
            'author': source_entry_['bibliography.author.name'].replace(',',
                                                                        ' '),
            'publication_year': source_entry_['bibliography.publication.year'],
        }

    with open(BOOK_SOURCE, 'r', newline='') as source:
        with open(BOOK_FILTERED, 'w', newline='') as filtered:
            csv_dict_reader = csv.DictReader(source)
            csv_dict_writer = csv.DictWriter(
                f=filtered,
                fieldnames=(
                'id', 'name', 'author', 'publication_year', 'type'),
            )
            csv_dict_writer.writeheader()
            for id_ in range(1, 101):
                source_entry = next(csv_dict_reader)
                filtered_entry = filter_book_entry(source_entry)
                while is_invalid_entry(filtered_entry):
                    source_entry = next(csv_dict_reader)
                    filtered_entry = filter_book_entry(source_entry)
                filtered_entry['id'] = str(id_)
                filtered_entry['type'] = str(randint(1, 3))
                csv_dict_writer.writerow(filtered_entry)
