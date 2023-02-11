VERSION ROADMAP
===============

v0.1.0-1 restructure docs
-------------------------

* Renamed old road map to ravings.
* Created new roadmap to contain a version roadmap.

v0.1.0-2 create django skeleton
-------------------------------

* Created project.
* Set shared templates dir.
* Created container html template.
* Created main app.
* Created index html page.
* Created index view.
* Created url mapping for main index view.

v0.1.0-3 Switch to following MDN "Local Library" Django tutorial
----------------------------------------------------------------

* Added note about the MDN tutorial to project README.md and to docs/index.rst .

v0.1.1-3 fix reStructuredText markup
------------------------------------

* Fixed link markup in index.rst to properly reStructuredText hyperlink markup.

v0.2.0 Adjusted project to fulfill MDN Django tutorial part 2
-------------------------------------------------------------

* Renamed main app to catalog app
* Adjusted settings to refer to catalog app.
* Changed timezone to Israel.
* Created utils/secret module for generating Django secret keys.
* Changed project secret key to use the above module.
* Removed Template dirs for now.
* Moved site root redirections to books_library/urls.
* Emptied catalog/urls and catalog/views for now.

v0.3.0 MDN tutorial part 3 (data model) & polls import
------------------------------------------------------

* Copied abstract data model from MDN tutorial.
* Created Django models according to the abstract data model.
* Applied migrations for the catalog data models.
* Copied site index app from my Django scratchpad in the JBA repo.
* Copied user manager app from my Django scratchpad in the JBA repo.
* Copied polls app from my Django scratchpad in the JBA repo.
* Copied some Django settings from my Django scratchpad in the JBA repo.

v0.3.1 MDN tutorial data model adjustment to 7k books dataset
-------------------------------------------------------------

* Changed Book.author to Book.authors (ManyToManyField).
* Added Book.subtitle (CharField).
* Added Book.thumbnail (URLField).
* Added Book.publication_year (SmallPositiveIntegerField).
* Added Book.average_rating (DecimalField).
* Added Book.ratings_count (PositiveIntegerField).
* Added Book.num_pages (SmallPositiveIntegerField).
* Removed Book.Language .
* Removed Author.date_of_birth .
* Removed Author.date_of_death .
* Removed BookCopy.imprint .

v0.3.2 MDN tutorial extra data model adjustments
-------------------------------------------------------------

* Added auxiliary BooksAuthors table to prevent authors with books from being deleted.
* Moved LoanStatus into BookCopy
* Reformatted LoanStatus to use Django's TextChoices.

v0.4.0 MDN tutorial part 4 (admin site)
------------------------------------------------------

* Registered catalog models with admin site.
