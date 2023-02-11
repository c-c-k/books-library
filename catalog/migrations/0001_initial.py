# Generated by Django 4.1.6 on 2023-02-11 14:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name of the book author.', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(help_text='Enter the book\'s 13 digit ISBN.see <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a> for details.', max_length=13, unique=True, verbose_name='ISBN')),
                ('title', models.CharField(help_text="Enter the book's title.", max_length=256)),
                ('subtitle', models.CharField(blank=True, help_text="Enter the book's subtitle,can be left empty.", max_length=256, null=True)),
                ('publication_year', models.PositiveSmallIntegerField(help_text="Enter the year of the book's publication.")),
                ('thumbnail', models.URLField(blank=True, help_text='Enter a url for the books thumbnail picture,can be left blank.', max_length=256, null=True)),
                ('summary', models.TextField(blank=True, help_text='Enter a short summary of the book,can be left empty.', max_length=1024, null=True)),
                ('page_count', models.PositiveSmallIntegerField(help_text='Enter the number of pages in the book.')),
                ('average_rating', models.DecimalField(decimal_places=2, default=5, help_text='Enter a previously known user rating,can be left blank.', max_digits=4)),
                ('ratings_count', models.PositiveIntegerField(default=0, help_text='Enter a previously known count of user ratings,can be left blank.')),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name of the genre (e.g. fiction, historical, etc..).', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='BooksAuthors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='catalog.author')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.book')),
            ],
        ),
        migrations.CreateModel(
            name='BookCopy',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='A unique id for the book copy across the whole library.', primary_key=True, serialize=False)),
                ('due_back', models.DateField(blank=True, help_text="Enter the date by which the book should be returned if it's on loan, leave blank if the book is not currently on loan.", null=True)),
                ('status', models.CharField(blank=True, choices=[('A', 'Available'), ('L', 'On Loan'), ('R', 'Reserved'), ('M', 'Maintenance')], default='M', help_text='Book Availability', max_length=1)),
                ('book', models.ForeignKey(help_text="Choose the book copy's general information entry.", on_delete=django.db.models.deletion.RESTRICT, to='catalog.book')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(help_text="Choose the book's author/s.", through='catalog.BooksAuthors', to='catalog.author'),
        ),
        migrations.AddField(
            model_name='book',
            name='categories',
            field=models.ForeignKey(help_text='Choose the genres to which the book belongs.', on_delete=django.db.models.deletion.RESTRICT, to='catalog.categories'),
        ),
    ]
