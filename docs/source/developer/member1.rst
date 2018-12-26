.. include:: <isonum.txt>
.. role:: sql(code)
   :language: sql
   :class: highlight


Parts Implemented by Ahmed Yasin KUL
=====================================


**Main Tables**
***************


Person Table
------------

This table is to hold a person's information which are available for all
people. Both ``Customer`` and ``Author`` tables are uses this table to store
common information (such as ``name``, ``surname``, ``gender`` etc.) for both
customers and authors.


Attributes of Person Table
^^^^^^^^^^^^^^^^^^^^^^^^^^

* :sql:`PERSON_ID`
    - :sql:`PRIMARY KEY`
    - *Type:* :sql:`SERIAL`
    - *Explanation:* Primary key of the Person table.
* :sql:`PERSON_NAME`
    - *Type:* :sql:`VARCHAR(50)`
    - *Explanation:* Name of the person.
    - *Nullable:* :sql:`NOT NULL`
* :sql:`SURNAME`
    - *Type:* :sql:`VARCHAR(50)`
    - *Explanation:* Surname of the person.
    - *Nullable:* :sql:`NOT NULL`
* :sql:`GENDER`
    - *Type:* :sql:`GENDER_TYPE`
    - *Explanation:* Gender of the person.
    - *Explanation about type:* It's type is a created domain which accepts
      only one of these three characters:

    =========  ======  =============
    Value: F   |rarr|  Female
    Value: M   |rarr|  Male
    Value: O   |rarr|  Not Specified
    =========  ======  =============

* :sql:`DATE_OF_BIRTH`
    - *Type:* :sql:`DATE`
    - *Explanation:* Date of birth of the person.
* :sql:`NATIONALITY`
    - *Type:* :sql:`VARCHAR(50)`
    - *Explanation:* Nationality of the person.


Code of Person Table
^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: /../../table_operations/person.py
   :language: python
   :linenos:
   :caption: Person Class
   :name: PersonClass
   :lines: 1-16

Here in ``__init__`` function, ``Person`` class initializes
its parent class (``baseClass``) with ``table_name`` = ``PERSON``
and ``cons`` = ``PersonObj``.

In ``add`` function, it calls ``insertIntoFlex`` (which is introduced
in `baseClass <baseClass.rst#baseclass-insertintoflex>`__ part of
documentation) by giving its columns' names as arguments. This function
adds these column names to an :sql:`INSERT INTO` SQL statement and returns
this string. Then additionally, this function adds :sql:`RETURNING PERSON_ID`
to this returned string to take the last added person's ID from database
(this will be used by customer and author classes). After that, it calls
``execute`` function with values that are given as arguments to this function.




Customer Table
--------------

This table is to hold customers' information that are not available in
``Person`` table such as ``username``, ``email``, ``pass_hash`` etc.
These information are not available in ``Person`` table because also
``Author`` table is derived from ``Person`` table and these columns are
not valid (available) for ``Author`` instances. Thus, this table stores
these kinds of information related with customers and also refers to
``Person`` table by its :sql:`PERSON_ID` column.


Attributes of Customer Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :sql:`CUSTOMER_ID`
    - :sql:`PRIMARY KEY`
    - *Type:* :sql:`SERIAL`
    - *Explanation:* Primary key of the Customer table.
* :sql:`PERSON_ID`
    - *Type:* :sql:`INTEGER`
    - *Explanation:* Customer's attributes such as name, surname, gender etc.
      are stored in Person table. So this field is to point these records
      on Person table.
    - *Unique:* :sql:`UNIQUE`
    - *Nullable:* :sql:`NOT NULL`
    - *Reference:* :sql:`PERSON (PERSON_ID)`
* :sql:`USERNAME`
    - *Type:* :sql:`VARCHAR(20)`
    - *Explanation:* Username of the customer.
    - *Unique:* :sql:`UNIQUE`
    - *Nullable:* :sql:`NOT NULL`
* :sql:`EMAIL`
    - *Type:* :sql:`VARCHAR(50)`
    - *Explanation:* E-mail address of the customer.
    - *Unique:* :sql:`UNIQUE`
    - *Nullable:* :sql:`NOT NULL`
* :sql:`PASS_HASH`
    - *Type:* :sql:`CHAR(87)`
    - *Explanation:* Customer's password string with hashed SHA256.
    - *Nullable:* :sql:`NOT NULL`
* :sql:`PHONE`
    - *Type:* :sql:`CHAR(10)`
    - *Explanation:* Phone number of the customer.
    - *Unique:* :sql:`UNIQUE`
    - *Nullable:* :sql:`NOT NULL`
* :sql:`IS_ACTIVE`
    - *Type:* :sql:`BOOLEAN`
    - *Explanation:* This field shows that the
      customer's account is whether active or passive state.
    - *Default:* :sql:`TRUE`


Code of Customer Table
^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: /../../table_operations/customer.py
   :language: python
   :linenos:
   :caption: Customer Class
   :name: CustomerClass
   :lines: 1-16

Here in ``__init__`` function, ``Customer`` class initializes
its parent class (``baseClass``) with ``table_name`` = ``CUSTOMER``
and ``cons`` = ``CustomerObj``.

In ``add`` function, it calls ``insertIntoFlex`` (which is introduced
in `baseClass <baseClass.rst#baseclass-insertintoflex>`__ part of
documentation) by giving its columns' names as arguments. This function
adds these column names to an :sql:`INSERT INTO` SQL statement and returns
this string. Then additionally, this function adds :sql:`RETURNING CUSTOMER_ID`
to this returned string to take the last added person's ID from database
(this will be used in operations). After that, it calls ``execute`` function
with values that are given as arguments to this function.




Address Table
-------------

This table is to hold customers' addresses to specify delivery addresses of
orders and also to provide quicker order placement for customers (as they
can access their previously saved addresses easily by the help of this table).


Attributes of Address Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :sql:`ADDRESS_ID`
    - :sql:`PRIMARY KEY`
    - *Type:* :sql:`SERIAL`
    - *Explanation:* Primary key of the Address table.
* :sql:`ADDRESS_NAME`
    - *Type:* :sql:`VARCHAR(30)`
    - *Explanation:* Meaningful name of the address entry that
      will be used when an order is placing by customer to select
      his/her desired address.
* :sql:`COUNTRY`
    - *Type:* :sql:`VARCHAR(30)`
    - *Explanation:* Country of the address.
    - *Nullable:* :sql:`NOT NULL`
* :sql:`CITY`
    - *Type:* :sql:`VARCHAR(30)`
    - *Explanation:* City of the address.
    - *Nullable:* :sql:`NOT NULL`
* :sql:`DISTRICT`
    - *Type:* :sql:`VARCHAR(30)`
    - *Explanation:* District of the address.
* :sql:`NEIGHBORHOOD`
    - *Type:* :sql:`VARCHAR(30)`
    - *Explanation:* Neighborhood of the address.
* :sql:`AVENUE`
    - *Type:* :sql:`VARCHAR(30)`
    - *Explanation:* Avenue of the address.
* :sql:`STREET`
    - *Type:* :sql:`VARCHAR(30)`
    - *Explanation:* Street of the address.
* :sql:`ADDR_NUMBER`
    - *Type:* :sql:`VARCHAR(10)`
    - *Explanation:* Building number of the address that is described.
* :sql:`ZIPCODE`
    - *Type:* :sql:`CHAR(5)`
    - *Explanation:* Zipcode of the building.
* :sql:`EXPLANATION`
    - *Type:* :sql:`VARCHAR(500)`
    - *Explanation:* Explanation for the address.


Code for Address Table
^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: /../../table_operations/address.py
   :language: python
   :linenos:
   :caption: Address Class
   :name: AddressClass
   :lines: 1-15

Here in ``__init__`` function, ``Address`` class initializes
its parent class (``baseClass``) with ``table_name`` = ``ADDRESS``
and ``cons`` = ``AddressObj``.

In ``add`` function, it calls ``insertIntoFlex`` (which is introduced
in `baseClass <baseClass.rst#baseclass-insertintoflex>`__ part of
documentation) by giving its columns' names as arguments. This function
adds these column names to an :sql:`INSERT INTO` SQL statement and returns
this string. After that, it calls ``execute`` function with values that are
given as arguments to this function.



**Additional Tables**
*********************


Author Table
------------

This table is to store authors' extra information that are not stored in
``Person`` table and it also refers to ``Person`` table by its ``PERSON_ID``
column.


Attributes of Author Table
^^^^^^^^^^^^^^^^^^^^^^^^^^

* :sql:`AUTHOR_ID`
    - :sql:`PRIMARY KEY`
    - *Type:* :sql:`SERIAL`
    - *Explanation:* Primary key of the Author table.
* :sql:`PERSON_ID`
    - *Type:* :sql:`INTEGER`
    - *Explanation:* Author's attributes such as name, surname, gender etc.
      are stored in Person table. So this field is to point these records
      on Person table.
    - *Reference:* :sql:`PERSON (PERSON_ID)`
* :sql:`BIOGRAPHY`
    - *Type:* :sql:`VARCHAR(1000)`
    - *Explanation:* Biography of the author.



Code of Author Table
^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: /../../table_operations/author.py
   :language: python
   :linenos:
   :caption: Author Class
   :name: AuthorClass
   :lines: 1-11

Here in ``__init__`` function, ``Author`` class initializes
its parent class (``baseClass``) with ``table_name`` = ``AUTHOR``
and ``cons`` = ``AuthorObj``.

In ``add`` function, it calls ``insertIntoFlex`` (which is introduced
in `baseClass <baseClass.rst#baseclass-insertintoflex>`__ part of
documentation) by giving its columns' names as arguments. This function
adds these column names to an :sql:`INSERT INTO` SQL statement and returns
this string. After that, it calls ``execute`` function with values that are
given as arguments to this function.



Book_Author Table
-----------------

This table is to map books with authors. Due to a book can have more than
one author, we have needed this table. Since this table stores books' IDs
and corresponding authors' IDs, a book's authors' can easily be found
by the help of this table.


Attributes of Book_Author Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:sql:`PRIMARY KEY (BOOK_ID, AUTHOR_ID)`

* :sql:`BOOK_ID`
    - *Type:* :sql:`INTEGER`
    - *Explanation:* To specify which book is related with this record.
    - *Reference:* :sql:`BOOK (BOOK_ID)`
* :sql:`AUTHOR_ID`
    - *Type:* :sql:`INTEGER`
    - *Explanation:* To specify which author is related with this record.
    - *Reference:* :sql:`AUTHOR (AUTHOR_ID)`


Code of Book_Author Table
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: /../../table_operations/book_author.py
   :language: python
   :linenos:
   :caption: Book_Author Class
   :name: BookAuthorClass
   :lines: 1-11

Here in ``__init__`` function, ``Book_Author`` class initializes
its parent class (``baseClass``) with ``table_name`` = ``BOOK_AUTHOR``
and ``cons`` = ``Book_AuthorObj``.

In ``add`` function, it calls ``insertIntoFlex`` (which is introduced
in `baseClass <baseClass.rst#baseclass-insertintoflex>`__ part of
documentation) by giving its columns' names as arguments. This function
adds these column names to an :sql:`INSERT INTO` SQL statement and returns
this string. After that, it calls ``execute`` function with values that are
given as arguments to this function.




Category Table
--------------

This table is to store categories' information (categories' names).


Attributes of Category Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :sql:`CATEGORY_ID`
    - :sql:`PRIMARY KEY`
    - *Type:* :sql:`SERIAL`
    - *Explanation:* Primary key of the Category table.
* :sql:`CATEGORY_NAME`
    - *Type:* :sql:`VARCHAR(50)`
    - *Explanation:* Name of the category.
    - *Unique:* :sql:`UNIQUE` (Since we don't want to add same categories
      for every execution of ``dbinit.py`` file and we have no another unique
      attribute that distincts categories from each other, we have set this
      attribute as unique.)


Code of Category Table
^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: /../../table_operations/category.py
   :language: python
   :linenos:
   :caption: Category Class
   :name: CategoryClass
   :lines: 1-11

Here in ``__init__`` function, ``Category`` class initializes
its parent class (``baseClass``) with ``table_name`` = ``CATEGORY``
and ``cons`` = ``CategoryObj``.

In ``add`` function, the :sql:`INSERT INTO` SQL statement for this table
has already stated as ``query`` variable. Thus, this function only calls
``execute`` function with this ``query`` variable and ``category_name``
argument that is given to the function.




Book_Category Table
-------------------

This table is to map books with categories. Due to a book can have more than
one category, we have needed this table. Since, this table stores books' IDs
and corresponding categories' IDs, a book's categories' can easily be found
by the help of this table.


Attributes of Book_Category Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:sql:`PRIMARY KEY (BOOK_ID, CATEGORY_ID)`

* :sql:`BOOK_ID`
    - *Type:* :sql:`INTEGER`
    - *Explanation:* To specify which book is related with this record.
    - *Reference:* :sql:`BOOK (BOOK_ID)`
* :sql:`CATEGORY_ID`
    - *Type:* :sql:`INTEGER`
    - *Explanation:* To specify which category is related with this record.
    - *Reference:* :sql:`CATEGORY (CATEGORY_ID)`


Code of Book_Category Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: /../../table_operations/book_category.py
   :language: python
   :linenos:
   :caption: Book_Category Class
   :name: BookCategoryClass
   :lines: 1-11

Here in ``__init__`` function, ``Book_Category`` class initializes
its parent class (``baseClass``) with ``table_name`` = ``BOOK_CATEGORY``
and ``cons`` = ``Book_CategoryObj``.

In ``add`` function, it calls ``insertIntoFlex`` (which is introduced
in `baseClass <baseClass.rst#baseclass-insertintoflex>`__ part of
documentation) by giving its columns' names as arguments. This function
adds these column names to an :sql:`INSERT INTO` SQL statement and returns
this string. After that, it calls ``execute`` function with values that are
given as arguments to this function.














