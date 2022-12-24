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

STAGE 1 - PROJECT ABSTRACT OUTLINE:
-----------------------------------

* Copy the original project assignment file to the docs dir.
* Copy the original project assignment into this file for easier access.
* Based on the original assignment write MVC abstracts:
    - Model abstract.
    - View abstract.
    - Controller abstract.
* Add/update stage 2 action plan.

STAGE 2 - IMPLEMENTATION ABSTRACT OUTLINE:
------------------------------------------

* Based on the original assignment and MVC abstracts write abstract implementation outline:
    - Model abstract implementation outline.
    - View abstract implementation outline.
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

MODEL ABSTRACT
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
