import csv
import datetime
from pathlib import Path
from pprint import pprint
from random import randint

BOOK_SOURCE = Path('./classics.csv')
BOOK_FILTERED = Path('./books.csv')
CLIENT_SOURCE = Path('./customers-100.csv')
CLIENT_FILTERED = Path('./clients.csv')
LOAN_DATA = Path('./loans.csv')


def print_csv_headers(csv_file: Path):
    with open(csv_file, 'r', newline='') as csv_io:
        csv_dict = csv.DictReader(csv_io)
        pprint(next(csv_dict))


def extract_book_data():
    def is_invalid_entry(entry: dict):
        name = entry['name']
        return (',' in name) or (';' in name)

    def filter_book_entry(source_entry_: dict) -> dict:
        return {
            'name': source_entry_['bibliography.title'],
            'author': source_entry_['bibliography.author.name'].replace(',', ' '),
            'publication_year': source_entry_['bibliography.publication.year'],
        }

    with open(BOOK_SOURCE, 'r', newline='') as source:
        with open(BOOK_FILTERED, 'w', newline='') as filtered:
            csv_dict_reader = csv.DictReader(source)
            csv_dict_writer = csv.DictWriter(
                f=filtered,
                fieldnames=('id', 'name', 'author', 'publication_year', 'type'),
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


def extract_client_data():
    with open(CLIENT_SOURCE, 'r', newline='') as source:
        def filter_client_entry(source_entry_: dict) -> dict:
            return {
                'name': ' '.join((
                    source_entry_['First Name'],
                    source_entry_['Last Name'])),
                'city': source_entry_['City'],
            }

        with open(CLIENT_FILTERED, 'w', newline='') as filtered:
            csv_dict_reader = csv.DictReader(source)
            csv_dict_writer = csv.DictWriter(
                f=filtered,
                fieldnames=('id', 'name', 'city', 'age'),
            )
            csv_dict_writer.writeheader()
            for id_ in range(1, 101):
                source_entry = next(csv_dict_reader)
                filtered_entry = filter_client_entry(source_entry)
                filtered_entry['id'] = str(id_)
                filtered_entry['age'] = str(randint(6, 120))
                csv_dict_writer.writerow(filtered_entry)


def gen_loan_data():
    date_format = '%d/%m/%y'
    def gen_loan_date(
            base: datetime.datetime = datetime.datetime.now()
    ) -> datetime.datetime:
        recent = randint(1, 100) <= 60  # 60% chance for a recent loan
        if recent:
            offset = datetime.timedelta(days=randint(1, 7))
        else:
            offset = datetime.timedelta(weeks=randint(2, 200))
        return base - offset

    def gen_return_date(
            loan_date_: datetime.datetime
    ) -> datetime.datetime:
        offset = datetime.timedelta(days=randint(1, 14))
        return loan_date_ + offset

    with open(LOAN_DATA, 'w', newline='') as loans_file:
        csv_dict_writer = csv.DictWriter(
            f=loans_file,
            fieldnames=('customer id', 'book id', 'loan date', 'return date')
        )
        csv_dict_writer.writeheader()
        for _ in range(100):
            loan_date = gen_loan_date()
            return_date = gen_return_date(loan_date)
            entry = {
                'customer id': str(randint(1, 100)),
                'book id': str(randint(1, 100)),
                'loan date': loan_date.strftime(date_format),
                'return date': return_date.strftime(date_format)
            }
            csv_dict_writer.writerow(entry)


def main():
    # print_csv_headers(BOOK_SOURCE)
    # extract_book_data()
    # print_csv_headers(CLIENT_SOURCE)
    # extract_client_data()
    gen_loan_data()


if __name__ == '__main__':
    main()
