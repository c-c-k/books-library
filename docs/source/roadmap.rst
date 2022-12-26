========================================================================
Roadmap for: Books Library Project
========================================================================

A vague roadmap for doing this project.

========================================================================

========================================================================
001 - ACTION PLAN
========================================================================

STAGE 0 - GLOBAL NOTES:
-----------------------

* Start from the first step of the first stage.
* Don't get distracted, focus on one step at a time.
* If a thought or an idea pertaining to another step comes up, add it to these global notes, move it to the appropriate step while introspecting the whole, and, deal with it only when dealing with the relevant step.
* If the current step becomes impossible or too hard, reflect on previous step or steps that might be the root of the problem and start fixing things from there.
* Don't Panic.
* Potential TODOS:
    * By Teacher's suggestion/instructions:
        * Read on class factories vs composition vs inheritance.
        * Use class factories.
        * Use class composition.
        * Read on and use singleton/s.
        * Add digital/audio/softcover/hardcover to book specifications.
    * Logging...

STAGE 1 - PROJECT ABSTRACT OUTLINE:
-----------------------------------

* Copy the original project assignment file to the docs dir.
* Copy the original project assignment into this file for easier access.
* Based on the original assignment write MVC abstracts:
    - DAL abstract.
    - VIEW abstract.
    - Controller abstract.
* Add/update stage 2 action plan.

STAGE 2 - IMPLEMENTATION ABSTRACT OUTLINE:
------------------------------------------

* Based on the original assignment and MVC abstracts write abstract implementation outline:
    - DAL abstract implementation outline.
    - VIEW abstract implementation outline.
    - Controller abstract implementation outline.
* Add/update stage 3 action plan.

========================================================================

========================================================================
002 - ORIGINAL PROJECT ASSIGNMENT
========================================================================

In this project you will implement a simple system to manage books library

    1. Create 3 files representing 3 tables:
        *  Books
            *  Id (PK)
            *  Name
            *  Author
            *  Year Published
            *  Type (1/2/3)
        *  Customers
            *  Id (PK)
            *  Name
            *  City
            *  Age
        *  Loans
            *  CustID
            *  BookID
            *  Loandate
            *  Returndate

    2. The book type set the maximum loan time for the book:
        *  1 – up to 10 days
        *  2 – up to 5 days
        *  3 – up to 2 days

    3. Create the DAL:
        *  Build a class for each entity
        *  Create a separate module for each class
        *  Build unit tests

    4. Build a client application to use the DAL. Add the following operations (display a simple menu)
        *  Add a new customer
        *  Add a new book
        *  Loan a book
        *  Return a book
        *  Display all books
        *  Display all customers
        *  Display all loans
        *  Display late loans
        *  Find book by name
        *  Find customer by name
        *  Remove book
        *  Remover customer

========================================================================

========================================================================
003 - MVC ABSTRACT
========================================================================

DAL ABSTRACT
-----------------------

*  Books
    *  Id (PK)
    *  Name
    *  Author
    *  Year Published
    *  Type (1/2/3) (determines the maximum loan time for the book)
        *  1 – up to 10 days
        *  2 – up to 5 days
        *  3 – up to 2 days
*  Customers
    *  Id (PK)
    *  Name
    *  City
    *  Age
*  Loans
    *  CustID
    *  BookID
    *  Loandate
    *  Returndate

VIEW ABSTRACT
-----------------------

* Use simple menu interface.
* 1 to 1 relation with controller.
* No submenu's or anything fancy.

CONTROLLER ABSTRACT
-----------------------

* Actions:
    *  Add a new customer
    *  Add a new book
    *  Loan a book
    *  Return a book
    *  Remove book
    *  Remover customer
* Information:
    *  Display all books
    *  Display all customers
    *  Display all loans
    *  Display late loans
    *  Find book by name
    *  Find customer by name

========================================================================

========================================================================
004 - IMPLEMENTATION ABSTRACT OUTLINE:
========================================================================

004.1 - PERSISTENT STORAGE
------------------

* Use shelve module for persistent data storage.

004.2 - PACKAGE/DIRECTORY STRUCTURE
---------------------------

* books_library (application root directory)
    * data
        * (shelve shelf files ...)
    * dal
        * base.py
        * books.py
        * customers.py
        * loans.py
    * view
        * messages.py
        * menu.py
        * cli.py
    * controller.py
    * __main__.py


004.3 - DAL
---

* dal/base.py
    * class Field
        * basic descriptor/validator
    * class StrField(Field)
        * Validates that input value is a str.
    * class IntField(Field)
        * Validates that input value is an int.
    * class ChoiceField(Field)
        * Validates that input value is one of the allowed choices.
    * class PKField(IntField)
        * Adds a class attribute _next_id.
        * In case a new object is initialized with an Id, checks and adjusts the classes _next_id to be no smaller than the new objects Id.
        * In case a new object is created without an Id, add a new Id based on _next_id.
    * class FKField(IntField)
        * Takes as input only another object with a PKField attribute.
    * class DateField(Field)
        * Validates that input can be converted to a datetime.date object.
        * String conversion format/s are hardcoded.
    * class Model(dataclass)
        * Place-holder parent class for the book/client/loan models in case some shared base functionality is needed later on.
    * class Container
        * Interacts with persistent storage container.
            * Name of persistent storage container matches subclass name.
        * Has _model_class attribute that subclasses must override with the appropriate model.
        * get_all method
            * Returns an iterator over all of the items in the container.
        * add method
            * Adds a new item to the container.
    * class WithNameContainer(Container)
        * get_by_name method
            * Returns an iterator over all items with a name field equalling or containing the input name.
    * class WithRemoveContainer(Container)
        * remove method
            * Removes an item from the container.


* dal/books.py
   * class Book(Model)
       * id : PKField
       * name : StrField
       * author : StrField
       * year_published : IntField
       * type : ChoiceField (1, 2, 3)
       * _loan_types: dict { 1: 10, 2: 5, 3: 2 }
       * property loan_duration
           * returns the maximal loan duration according to book type.
   *class Books(WithNameContainer, WithRemoveContainer)
       * _model_type = Book

* dal/customers.py
   * class Customer(Model)
       * id : PKField
       * name : StrField
       * city : StrField
       * age : IntField
   *class Customers(WithNameContainer, WithRemoveContainer)
       * _model_type = Customer

* dal/loans.py
   * class Loan(Model)
       * customer_id : FKField
       * book_id : FKField
       * loan_date : DateField
       * return_date : DateField
       * property return_date
           * contains the expected maximal return date according to the loan date and the book type.
   *class Loans(Container)
       * _model_type = Loan
       * method get_overdue
           * returns an iterator over all overdue loans.

004.4 - VIEW IMPLEMENTATION ABSTRACT
----------------------------

* Use simple menu interface.
* 1 to 1 relation with controller.
* No submenu's or anything fancy.

004.4 - CONTROLLER IMPLEMENTATION ABSTRACT
----------------------------------

* Actions:
    *  Add a new customer
    *  Add a new book
    *  Loan a book
    *  Return a book
    *  Remove book
    *  Remover customer
* Information:
    *  Display all books
    *  Display all customers
    *  Display all loans
    *  Display late loans
    *  Find book by name
    *  Find customer by name

========================================================================

