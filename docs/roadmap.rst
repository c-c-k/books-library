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
