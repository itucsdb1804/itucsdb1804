Parts Implemented by Muhammed YILMAZ
=====================================

**Main Tables**
***************

.. _BOOK_EDITION_TABLE:

BOOK_EDITION Table
------------------

A book has more than one edition. This table keeps the information of book
prints.

Attributes of BOOK_EDITION Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+-----------------+--------------+
| ATTRIBUTE NAME  | TYPE         |
+=================+==============+
| BOOK_ID         | INTEGER      |
+-----------------+--------------+
| EDITION_NUMBER  | SMALLINT     |
+-----------------+--------------+
| ISBN            | VARCHAR(20)  |
+-----------------+--------------+
| PUBLISHER       | VARCHAR(100) |
+-----------------+--------------+
| PUBLISH_YEAR    | SMALLINT     |
+-----------------+--------------+
| NUMBER_OF_PAGES | SMALLINT     |
+-----------------+--------------+
| LANGUAGE        | VARCHAR(50)  |
+-----------------+--------------+

- **PRIMARY KEY:** ``BOOK_ID`` + ``EDITION_NUMBER``
- **FOREIGN KEY:** ``BOOK_ID`` REFERENCES ``BOOK`` TABLE,
  see BOOK_TABLE_

Code of BOOK_EDITION Table
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:
    :lineno-start: 11
    :caption: **2.1.1: Book Edition - Insert Function** (file: ``table_operations/book_edition.py``, version: ``d1dcbe9``)
    :name: be-insert-code

    def add(self, book_edition):
        query = "INSERT INTO BOOK_EDITION (BOOK_ID, EDITION_NUMBER, ISBN, PUBLISHER, PUBLISH_YEAR, NUMBER_OF_PAGES, LANGUAGE) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        fill = (book_edition.book_id, book_edition.edition_number, book_edition.isbn, book_edition.publisher, book_edition.publish_year, book_edition.number_of_pages, book_edition.language)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

        return book_edition.book_id, book_edition.edition_number

This function takes the object ``BookEditionObj`` as the argument. The
function executes the sql query by filling the ``INSERT INTO`` query it
creates for the ``BOOK_EDITION`` table with the information in the
``book_edition`` object. The function returns ``book_id`` and
``edition_number``.

.. code-block:: python
    :linenos:
    :lineno-start: 22
    :caption: **2.1.2: Book Edition - Update Function** (file: ``table_operations/book_edition.py``, version: ``d1dcbe9``)
    :name: be-update-code

    def update(self, update_columns, new_values, where_columns, where_values):
        self.updateGeneric(update_columns, new_values, where_columns, where_values)

This function uses ``updateGeneric`` function of baseClass.
See `baseClass <baseClass.html>`__ for more.

.. code-block:: python
    :linenos:
    :lineno-start: 25
    :caption: **2.1.3: Book Edition - Delete Function** (file: ``table_operations/book_edition.py``, version: ``d1dcbe9``)
    :name: be-delete-code

    def delete(self, book_id, edition_number):
        query = "DELETE FROM BOOK_EDITION WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

This function takes the primary key of the ``BOOK_EDITION`` table,
``book_id`` and ``edition_number``, as an argument. The function
executes the ``DELETE`` query that is written for the ``BOOK_EDITION``
table by filling it with ``book_id`` and ``edition_number``.


.. code-block:: python
    :linenos:
    :lineno-start: 34
    :caption: **2.1.4: Book Edition - Get Row Function** (file: ``table_operations/book_edition.py``, version: ``d1dcbe9``)
    :name: be-getRow-code

    def get_row(self, book_id, edition_number):
        _book_edition = None

        query = "SELECT * FROM BOOK_EDITION WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            book_edition = cursor.fetchone()
            if book_edition is not None:
                _book_edition = BookEditionObj(book_edition[0], book_edition[1], book_edition[2], book_edition[3], book_edition[4], book_edition[5], book_edition[6])

        return _book_edition

This function takes the primary key of the ``BOOK_EDITION`` table,
``book_id`` and ``edition_number``, as an argument. The function executes
the ``SELECT`` query that is written for the ``BOOK_EDITION`` table
by filling it with ``book_id`` and ``edition_number`` and returns
object of ``BookEditionObj`` that is found.

.. code-block:: python
    :linenos:
    :lineno-start: 49
    :caption: **2.1.5: Book Edition - Get Row by Book Function** (file: ``table_operations/book_edition.py``, version: ``d1dcbe9``)
    :name: be-getRowByBook-code

    def get_rows_by_book(self, book_id):
        book_edition_table = []
        if type(book_id) == int:
            book_id = str(book_id)

        query = "SELECT * FROM BOOK_EDITION WHERE (BOOK_ID = %s)"
        fill = (book_id,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            for book_edition in cursor:
                book_edition_ = BookEditionObj(book_edition[0], book_edition[1], book_edition[2], book_edition[3], book_edition[4], book_edition[5], book_edition[6])
                book_edition_table.append(book_edition_)
            cursor.close()

        return book_edition_table

This function takes the primary key of the ``BOOK_EDITION`` table,
``book_id`` and ``edition_number``, as an argument. The function executes
the ``SELECT`` query that is written for the ``BOOK_EDITION`` table
by filling it with ``book_id`` and ``edition_number`` and returns
the found ``BookEditionObj`` objects as a list.

.. code-block:: python
    :linenos:
    :lineno-start: 67
    :caption: **2.1.6: Book Edition - Get Table Function** (file: ``table_operations/book_edition.py``, version: ``d1dcbe9``)
    :name: be-getTable-code

    def get_table(self, select_columns="*", where_columns=None, where_values=None):
        return self.getTableGeneric(select_columns, where_columns, where_values)

This function uses ``getTableGeneric`` function of baseClass.
See `baseClass <baseClass.html>`__ for more.


COMMENT Table
-------------

Users can comment on books. These comments appear at the bottom of each book's
page. The comment can only changed by the owner of that comment. The deletion
can be done by both the user and the admin.

Attributes of COMMENT Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^
+-------------------+--------------+
| ATTRIBUTE NAME    | TYPE         |
+===================+==============+
| COMMENT_ID        | SERIAL       |
+-------------------+--------------+
| CUSTOMER_ID       | INTEGER      |
+-------------------+--------------+
| BOOK_ID           | INTEGER      |
+-------------------+--------------+
| COMMENT_TITLE     | VARCHAR(50)  |
+-------------------+--------------+
| COMMENT_STATEMENT | VARCHAR(500) |
+-------------------+--------------+
| ADDED_TIME        | TIMESTAMP    |
+-------------------+--------------+
| UPDATED_TIME      | TIMESTAMP    |
+-------------------+--------------+
| RATING            | RATE_TYPE    |
+-------------------+--------------+

- **PRIMARY KEY:** ``COMMENT_ID``
- **FOREIGN KEY:** ``BOOK_ID`` REFERENCES ``BOOK`` TABLE,
  see BOOK_TABLE_
- **FOREIGN KEY:** ``CUSTOMER_ID`` REFERENCES ``CUSTOMER`` TABLE

Code of COMMENT Table
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:
    :lineno-start: 10
    :caption: **2.2.1: Comment - Insert Function** (file: ``table_operations/comment.py``, version: ``d1dcbe9``)
    :name: com-insert-code

    def add(self, comment):
        query = "INSERT INTO COMMENT (CUSTOMER_ID, BOOK_ID, COMMENT_TITLE, COMMENT_STATEMENT, RATING) VALUES (%s, %s, %s, %s, %s)"
        fill = (comment.customer_id, comment.book_id, comment.comment_title, comment.comment_statement, comment.rating)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

This function takes the object ``CommentObj`` as the argument. The
function executes the sql query by filling the ``INSERT INTO`` query it
creates for the ``COMMENT`` table with the information in the
``comment`` object.

.. code-block:: python
    :linenos:
    :lineno-start: 19
    :caption: **2.2.2: Comment - Update Function** (file: ``table_operations/comment.py``, version: ``d1dcbe9``)
    :name: com-update-code

    def update(self, comment_id, comment):
        query = "UPDATE COMMENT SET CUSTOMER_ID = %s, BOOK_ID = %s, COMMENT_TITLE = %s, COMMENT_STATEMENT = %s, UPDATED_TIME = CURRENT_TIMESTAMP, RATING = %s WHERE COMMENT_ID = %s"
        fill = (comment.customer_id, comment.book_id, comment.comment_title, comment.comment_statement, comment.rating, comment_id)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

This function takes the ``comment_id`` that is primary key of the
``COMMENT`` table and ``comment`` is obtained in type ``CommentObj``
as an argument. The function executes the ``UPDATE`` query that is
written for the ``COMMENT`` table by filling it with ``comment_key``
and new values from ``comment`` object.

.. code-block:: python
    :linenos:
    :lineno-start: 28
    :caption: **2.2.3: Comment - Delete Function** (file: ``table_operations/comment.py``, version: ``d1dcbe9``)
    :name: com-delete-code

    def delete(self, comment_key):
        query = "DELETE FROM COMMENT WHERE COMMENT_ID = %s"
        fill = (comment_key,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

This function takes the primary key of the ``COMMENT`` table,
``comment_key``, as an argument. The function executes the
``DELETE`` query that is written for the ``COMMENT`` table
by filling it with ``comment_key``.

.. code-block:: python
    :linenos:
    :lineno-start: 37
    :caption: **2.2.4: Comment - Get Row Function** (file: ``table_operations/comment.py``, version: ``d1dcbe9``)
    :name: com-getRow-code

    def get_row(self, comment_key):
        _comment = None

        query = "SELECT * FROM COMMENT WHERE COMMENT_ID = %s"
        fill = (comment_key,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            comment = cursor.fetchone()
            if comment is not None:
                _comment = CommentObj(comment[1], comment[2], comment[3], comment[4], comment[7], added_time=comment[5], updated_time=comment[6], comment_id=comment[0])

        return _comment

This function takes the primary key of the ``COMMENT`` table,
``comment_key``, as an argument. The function executes
the ``SELECT`` query that is written for the ``COMMENT`` table
by filling it with ``comment_key`` and returns
object of ``CommentObj`` that is found.

.. code-block:: python
    :linenos:
    :lineno-start: 52
    :caption: **2.2.5: Comment - Get Table Function** (file: ``table_operations/comment.py``, version: ``d1dcbe9``)
    :name: com-getTable-code

    def get_table(self, book_id=None):
        comments = []

        query = "SELECT * FROM COMMENT"
        if book_id:
            query += " WHERE BOOK_ID = %s"
            fill = (book_id,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            if book_id:
                cursor.execute(query, fill)
            else:
                cursor.execute(query)
            for comment in cursor:
                comment_ = CommentObj(comment[1], comment[2], comment[3], comment[4], comment[7], added_time=comment[5], updated_time=comment[6], comment_id=comment[0])
                comments.append(comment_)
            cursor.close()

        return comments

This function takes the primary key of the ``COMMENT`` table,
``book_id``, as an argument. The function executes
the ``SELECT`` query that is written for the ``COMMENT`` table
by filling it with ``book_id`. If ``book_id`` is None, the function
returns all table. If book_id is not None, function returns only
comments of book which has this book_id.

.. _PRODUCT_TABLE:

PRODUCT Table
-------------

This table holds sales information of book editions.

Attributes of PRODUCT Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------+--------------+--------------+
| ATTRIBUTE NAME      | TYPE         | DEFAULT      |
+=====================+==============+==============+
| BOOK_ID             | INTEGER      |              |
+---------------------+--------------+--------------+
| EDITION_NUMBER      | SMALLINT     |              |
+---------------------+--------------+--------------+
| REMAINING           | SMALLINT     | 0            |
+---------------------+--------------+--------------+
| ACTUAL_PRICE        | FLOAT        |              |
+---------------------+--------------+--------------+
| NUMBER_OF_SELLS     | SMALLINT     | 0            |
+---------------------+--------------+--------------+
| PRODUCT_DATE_ADDED  | DATE         | CURRENT_DATE |
+---------------------+--------------+--------------+
| PRODUCT_EXPLANATION | VARCHAR(500) |              |
+---------------------+--------------+--------------+
| IS_ACTIVE           | BOOLEAN      | TRUE         |
+---------------------+--------------+--------------+

- **PRIMARY KEY:** ``BOOK_ID`` + ``EDITION_NUMBER``
- **FOREIGN KEY:** (``BOOK_ID`` + ``EDITION_NUMBER``) REFERENCES
  ``BOOK_EDITION`` TABLE, see BOOK_EDITION_TABLE_

Code of Product Table
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:
    :lineno-start: 10
    :caption: **2.3.1: Product - Insert Function** (file: ``table_operations/product.py``, version: ``d1dcbe9``)
    :name: product-insert-code

    def add(self, product):
        query = "INSERT INTO PRODUCT (BOOK_ID, EDITION_NUMBER, REMAINING, ACTUAL_PRICE, NUMBER_OF_SELLS, PRODUCT_EXPLANATION, IS_ACTIVE) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        fill = (product.book_id, product.edition_number, product.remaining, product.actual_price, product.number_of_sells, product.product_explanation, product.is_active)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

        return product.book_id, product.edition_number

This function takes the object ``ProductObj`` as the argument. The
function executes the sql query by filling the ``INSERT INTO`` query it
creates for the ``PRODUCT`` table with the information in the
``product`` object. The function returns ``book_id`` and
``edition_number``.

.. code-block:: python
    :linenos:
    :lineno-start: 21
    :caption: **2.3.2: Product - Update Function** (file: ``table_operations/product.py``, version: ``d1dcbe9``)
    :name: product-update-code

    def update(self, book_id, edition_number, product):
        query = "UPDATE PRODUCT SET REMAINING = %s, ACTUAL_PRICE = %s, NUMBER_OF_SELLS = %s, PRODUCT_EXPLANATION = %s, IS_ACTIVE = %s WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (product.remaining, product.actual_price, product.number_of_sells, product.product_explanation,
                product.is_active, book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

        return book_id, edition_number

This function takes the ``book_id`` and ``edition_number`` that are
primary key of the ``PRODUCT`` table and ``product`` is obtained in
type ``ProductObj`` as an argument. The function executes the ``UPDATE``
query that is written for the ``PRODUCT`` table by filling it with
``book_id``, ``edition_number``, and new values from ``product`` object.

.. code-block:: python
    :linenos:
    :lineno-start: 33
    :caption: **2.3.3: Product - Update Piece and Remaining Function** (file: ``table_operations/product.py``, version: ``d1dcbe9``)
    :name: product-updatePieceAndRemaining-code

    def update_piece_and_remainig(self, book_id, edition_number, new_remaining, new_sold):
        query = "UPDATE PRODUCT SET REMAINING = %s, NUMBER_OF_SELLS = %s WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (new_remaining, new_sold, book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

        return book_id, edition_number

This function takes the ``book_id`` and ``edition_number`` that are
primary key of the ``PRODUCT`` table and values of  ``new_remaining``
and ``new_sold`` as an argument. The function executes the ``UPDATE``
query that is written for the ``PRODUCT`` table by filling it with
``book_id``,``edition_number``,``new_remaining``, and ``new_sold``.

.. code-block:: python
    :linenos:
    :lineno-start: 44
    :caption: **2.3.4: Product - Delete Function** (file: ``table_operations/product.py``, version: ``d1dcbe9``)
    :name: product-delete-code

    def delete(self, book_id, edition_number):
        query = "DELETE FROM PRODUCT WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

This function takes the primary key of the ``PRODUCT`` table,
``book_id`` and ``edition_number``, as an argument. The function executes the
``DELETE`` query that is written for the ``PRODUCT`` table
by filling it with ``book_id`` and ``edition_number``.

.. code-block:: python
    :linenos:
    :lineno-start: 53
    :caption: **2.3.5: Product - Get Row Function** (file: ``table_operations/product.py``, version: ``d1dcbe9``)
    :name: product-getRow-code

    def get_row(self, book_id, edition_number):
        _product = None

        query = "SELECT * FROM PRODUCT WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            product = cursor.fetchone()
            if product is not None:
                _product = ProductObj(product[0], product[1], product[2], product[3], product[4], product[6], product[7], date_added=product[5])

        return _product

This function takes the primary key of the ``PRODUCT`` table,
``book_id`` and ``edition_number``, as an argument. The function executes
the ``SELECT`` query that is written for the ``PRODUCT`` table
by filling it with ``book_id`` and ``edition_number`` and returns
object of ``ProductObj`` that is found.

.. code-block:: python
    :linenos:
    :lineno-start: 68
    :caption: **2.3.6: Product - Get Table Function** (file: ``table_operations/product.py``, version: ``d1dcbe9``)
    :name: product-getTable-code

    def get_table(self):
        products = []

        query = "SELECT * FROM PRODUCT;"

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            for product in cursor:
                product_ = ProductObj(product[0], product[1], product[2], product[3], product[4], product[6], product[7], date_added=product[5])
                products.append(product_)
            cursor.close()

        return products

This function does not takes any argument. The function executes
the ``SELECT`` query that is written for the ``PRODUCT`` table
and returns the all ``ProductObj`` objects as a list.

.. code-block:: python
    :linenos:
    :lineno-start: 83
    :caption: **2.3.7: Product - Get Products with All Info Function** (file: ``table_operations/product.py``, version: ``d1dcbe9``)
    :name: product-getProductsWithAllInfo-code

    def get_products_all_info(self, book_id=None, edition_number=None, is_active=True):
        products_editions_books = []

        query = "SELECT * FROM PRODUCT, BOOK_EDITION, BOOK " \
                "WHERE ((PRODUCT.BOOK_ID = BOOK.BOOK_ID  " \
                "AND BOOK.BOOK_ID = BOOK_EDITION.BOOK_ID " \
                "AND BOOK_EDITION.EDITION_NUMBER = PRODUCT.EDITION_NUMBER) " \
                "AND (PRODUCT.IS_ACTIVE = %s"
        fill = [is_active]

        if book_id:
            query += " AND BOOK_ID = %s"
            fill.append(book_id)
        if book_id and edition_number:
            query += " AND EDITION_NUMBER = %s"
            fill.append(edition_number)
        query += "))"

        fill = tuple(fill)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            for all_info in cursor:
                product_ = ProductObj(all_info[0], all_info[1], all_info[2], all_info[3], all_info[4], all_info[6], all_info[7], date_added=all_info[5])
                book_editions_ = BookEditionObj(all_info[8], all_info[9], all_info[10], all_info[11], all_info[12], all_info[13], all_info[14])
                book_ = BookObj(all_info[15], all_info[16], all_info[17], all_info[18])
                products_editions_books.append([product_, book_editions_, book_])
            cursor.close()

        return products_editions_books

This function does not takes any argument. The function executes
the ``SELECT`` query that is written for the ``PRODUCT``, ``BOOK_EDITION``,
and ``BOOK`` tables and returns the all ``ProductObj``, ``BookEditionObj``,
and ``BookObj`` sets as a list.

**Additional Tables**
*********************

.. _BOOK_TABLE:

BOOK Table
----------

This table keeps the book information.

Attributes of BOOK Table
^^^^^^^^^^^^^^^^^^^^^^^^
+------------------+---------------+
| ATTRIBUTE NAME   | TYPE          |
+==================+===============+
| BOOK_ID          | SERIAL        |
+------------------+---------------+
| BOOK_NAME        | VARCHAR(100)  |
+------------------+---------------+
| RELEASE_YEAR     | SMALLINT      |
+------------------+---------------+
| BOOK_EXPLANATION | VARCHAR(1000) |
+------------------+---------------+

- **PRIMARY KEY:** ``BOOK_ID``

Code of BOOK Table
^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:
    :lineno-start: 10
    :caption: **2.4.1: Book - Insert Function** (file: ``table_operations/book.py``, version: ``d1dcbe9``)
    :name: book-insert-code

    def add_book(self, book):
        query = "INSERT INTO BOOK (BOOK_NAME, RELEASE_YEAR, BOOK_EXPLANATION) VALUES (%s, %s, %s)"
        fill = (book.book_name, book.release_year, book.explanation)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

        return self.get_table()[-1].book_id

This function takes the object ``BookObj`` as the argument. The
function executes the sql query by filling the ``INSERT INTO`` query it
creates for the ``BOOK`` table with the information in the
``book`` object. The function returns ``book_id``.

.. code-block:: python
    :linenos:
    :lineno-start: 21
    :caption: **2.4.2: Book - Update Function** (file: ``table_operations/book.py``, version: ``d1dcbe9``)
    :name: book-update-code

    def update(self, book_key, book):
        query = "UPDATE BOOK SET BOOK_NAME = %s, RELEASE_YEAR = %s, BOOK_EXPLANATION = %s WHERE BOOK_ID = %s"
        fill = (book.book_name, book.release_year, book.explanation, book_key)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

        return book_key

This function takes the ``book_key`` that is primary key of the
``BOOK`` table and ``book`` is obtained in type ``BookObj`` as
an argument. The function executes the ``UPDATE`` query that is
written for the ``BOOK`` table by filling it with ``book_key``
and new values from ``book`` object.

.. code-block:: python
    :linenos:
    :lineno-start: 32
    :caption: **2.4.3: Book - Delete Function** (file: ``table_operations/book.py``, version: ``d1dcbe9``)
    :name: book-delete-code

    def delete(self, book_key):

        query1 = "DELETE FROM BOOK_AUTHOR WHERE BOOK_ID = %s"
        query2 = "DELETE FROM BOOK_CATEGORY WHERE BOOK_ID = %s"
        query3 = "DELETE FROM BOOK WHERE BOOK_ID = %s"
        fill = (book_key,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query1, fill)
            cursor.execute(query2, fill)
            cursor.execute(query3, fill)
            cursor.close()

This function also deletes book-category and book-author relations.
The function takes the primary key of the ``BOOK``, ``BOOK_AUTHOR``,
and ``BOOK_CATEGORY`` tables, ``book_key``, as an argument.
The function executes the ``DELETE`` queries that are written for
the ``BOOK``, ``BOOK_AUTHOR``, and ``BOOK_CATEGORY`` tables
by filling it with ``book_key``.

.. code-block:: python
    :linenos:
    :lineno-start: 46
    :caption: **2.4.4: Book - Get Row Function** (file: ``table_operations/book.py``, version: ``d1dcbe9``)
    :name: book-getRow-code

    def get_row(self, book_key):
        _book = None

        query = "SELECT * FROM BOOK WHERE BOOK_ID = %s"
        fill = (book_key,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            book = cursor.fetchone()
            if book is not None:
                _book = BookObj(book[0], book[1], book[2], book[3])

        return _book

This function takes the primary key of the ``BOOK`` table,
``book_key``, as an argument. The function executes
the ``SELECT`` query that is written for the ``BOOK`` table
by filling it with ``book_key`` and returns
object of ``BookObj`` that is found.

.. code-block:: python
    :linenos:
    :lineno-start: 61
    :caption: **2.4.5: Book - Get Table Function** (file: ``table_operations/book.py``, version: ``d1dcbe9``)
    :name: book-getTable-code

    def get_table(self, select_columns="*", where_columns=None, where_values=None):
        return self.getTableGeneric(select_columns, where_columns, where_values)

This function uses ``getTableGeneric`` function of baseClass.
See `baseClass <baseClass.html>`__ for more.

.. _TRANSACTION_TABLE:

TRANSACTION Table
-----------------

This table keeps each member's shopping cart information. When a new customer
becomes a member of the system, an empty shopping cart is automatically
created. The customer who adds the products to the shopping cart chooses the
address and payment type before completing the exchange, adds a description
to the order and completes the order. When the order is complete, the
``IS_COMPLETED`` property of this order is ``true`` and the new empty shopping
cart is created.

Attributes of TRANSACTION Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------+--------------+---------+
| ATTRIBUTE NAME          | TYPE         | DEFAULT |
+=========================+==============+=========+
| TRANSACTION_ID          | SERIAL       |         |
+-------------------------+--------------+---------+
| CUSTOMER_ID             | INTEGER      |         |
+-------------------------+--------------+---------+
| ADDRESS_ID              | INTEGER      | NULL    |
+-------------------------+--------------+---------+
| TRANSACTION_TIME        | TIMESTAMP    | NULL    |
+-------------------------+--------------+---------+
| PAYMENT_TYPE            | VARCHAR(30)  | NULL    |
+-------------------------+--------------+---------+
| TRANSACTION_EXPLANATION | VARCHAR(200) | NULL    |
+-------------------------+--------------+---------+
| IS_COMPLETED            | BOOLEAN      | FALSE   |
+-------------------------+--------------+---------+

- **PRIMARY KEY:** ``TRANSACTION_ID``
- **FOREIGN KEY:** ``CUSTOMER_ID`` REFERENCES ``CUSTOMER`` TABLE
- **FOREIGN KEY:** ``ADDRESS_ID`` REFERENCES ``ADDRESS`` TABLE

Code of TRANSACTION Table
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:
    :lineno-start: 10
    :caption: **2.5.1: Transaction - Insert Function** (file: ``table_operations/transaction.py``, version: ``d1dcbe9``)
    :name: transaction-insert-code

    def add(self, transaction):
        query = "INSERT INTO TRANSACTION (CUSTOMER_ID, ADDRESS_ID, TRANSACTION_TIME, PAYMENT_TYPE, TRANSACTION_EXPLANATION) VALUES (%s, %s, %s, %s, %s)"
        fill = (transaction.customer_id, transaction.address_id, transaction.transaction_time, transaction.payment_type, transaction.explanation)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

This function takes the object ``TransactionObj`` as the argument. The
function executes the sql query by filling the ``INSERT INTO`` query it
creates for the ``TRANSACTION`` table with the information in the
``transaction`` object.

.. code-block:: python
    :linenos:
    :lineno-start: 19
    :caption: **2.5.2: Transaction - Insert Empity Row Function** (file: ``table_operations/transaction.py``, version: ``d1dcbe9``)
    :name: transaction-insertEmpityRow-code

    def add_empty(self, customer_id):
        query = "INSERT INTO TRANSACTION (CUSTOMER_ID) VALUES (%s)"
        fill = (customer_id,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

This function takes the object ``customer_id`` as the argument. The
function executes the sql query by filling the ``INSERT INTO`` query
it creates for the ``TRANSACTION`` table with ``customer_id``
as empity shopping cart.

.. code-block:: python
    :linenos:
    :lineno-start: 28
    :caption: **2.5.3: Transaction - Update Function** (file: ``table_operations/transaction.py``, version: ``d1dcbe9``)
    :name: transaction-update-code

    def update(self, update_columns, new_values, where_columns, where_values):
        self.updateGeneric(update_columns, new_values, where_columns, where_values)

This function uses ``updateGeneric`` function of baseClass.
See `baseClass <baseClass.html>`__ for more.

.. code-block:: python
    :linenos:
    :lineno-start: 31
    :caption: **2.5.4: Transaction - Delete Function** (file: ``table_operations/transaction.py``, version: ``d1dcbe9``)
    :name: transaction-delete-code

    def delete(self, transaction_key):
        query = "DELETE FROM TRANSACTION WHERE TRANSACTION_ID = %s"
        fill = (transaction_key,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

This function takes the primary key of the ``TRANSACTION`` table,
``transaction_key``, as an argument. The function executes the
``DELETE`` query that is written for the ``TRANSACTION`` table
by filling it with ``transaction_key``.

.. code-block:: python
    :linenos:
    :lineno-start: 40
    :caption: **2.5.5: Transaction - Get Row Function** (file: ``table_operations/transaction.py``, version: ``d1dcbe9``)
    :name: transaction-getRow-code

    def get_row(self, select_columns="*", where_columns=None, where_values=None):
        return self.getRowGeneric(select_columns, where_columns, where_values)

This function uses ``getRowGeneric`` function of baseClass.
See `baseClass <baseClass.html>`__ for more.

.. code-block:: python
    :linenos:
    :lineno-start: 43
    :caption: **2.5.6: Transaction - Get Table Function** (file: ``table_operations/transaction.py``, version: ``d1dcbe9``)
    :name: transaction-getTable-code

    def get_table(self):
        transactions = []

        query = "SELECT * FROM TRANSACTION;"

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            for transaction in cursor:
                transaction_ = TransactionObj(transaction[1], transaction[2], transaction[3], transaction[4], transaction[5])
                transactions.append((transaction[0], transaction_))
            cursor.close()

        return transactions

This function does not takes any argument. The function executes
the ``SELECT`` query that is written for the ``TRANSACTION`` table
and returns the all ``ProductObj`` objects in table as a list.

TRANSACTION_PRODUCT Table
-------------------------

This table keeps the information of the products in the shopping cart for
each customer. The customer can update or delete the product at any time.

Attributes of TRANSACTION_PRODUCT Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+----------------+-----------+
| ATTRIBUTE NAME | TYPE      |
+================+===========+
| TRANSACTION_ID | INTEGER   |
+----------------+-----------+
| BOOK_ID        | INTEGER   |
+----------------+-----------+
| EDITION_NUMBER | SMALLINT  |
+----------------+-----------+
| PIECE          | SMALLINT  |
+----------------+-----------+
| UNIT_PRICE     | FLOAT     |
+----------------+-----------+

- **PRIMARY KEY:** ``TRANSACTION_ID`` + ``BOOK_ID`` + ``EDITION_NUMBER``
- **FOREIGN KEY:** (``BOOK_ID`` + ``EDITION_NUMBER``) REFERENCES ``PRODUCT``
  TABLE, see PRODUCT_TABLE_
- **FOREIGN KEY:** ``TRANSACTION_ID`` REFERENCES ``TRANSACTION`` TABLE, see
  TRANSACTION_TABLE_

Code of TRANSACTION_PRODUCT Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:
    :lineno-start: 10
    :caption: **2.6.1: Transaction Product - Insert Function** (file: ``table_operations/transaction_product.py``, version: ``d1dcbe9``)
    :name: transactionProduct-insert-code

    def add(self, transaction_product):
        query = "INSERT INTO TRANSACTION_PRODUCT (TRANSACTION_ID, BOOK_ID, EDITION_NUMBER, PIECE, UNIT_PRICE) VALUES (%s, %s, %s, %s, %s)"
        fill = (transaction_product.transaction_id, transaction_product.book_id, transaction_product.edition_number, transaction_product.piece, transaction_product.unit_price)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)

This function takes the object ``Transaction_ProductObj`` as the argument.
The function executes the sql query by filling the ``INSERT INTO`` query it
creates for the ``TRANSACTION_PRODUCT`` table with the information in the
``transaction_product`` object.

.. code-block:: python
    :linenos:
    :lineno-start: 18
    :caption: **2.6.2: Transaction Product - Update Function** (file: ``table_operations/transaction_product.py``, version: ``d1dcbe9``)
    :name: transactionProduct-update-code

    def update(self, update_columns, new_values, where_columns, where_values):
        self.updateGeneric(update_columns, new_values, where_columns, where_values)

This function uses ``updateGeneric`` function of baseClass.
See `baseClass <baseClass.html>`__ for more.

.. code-block:: python
    :linenos:
    :lineno-start: 21
    :caption: **2.6.3: Transaction Product - Delete Function** (file: ``table_operations/transaction_product.py``, version: ``d1dcbe9``)
    :name: transactionProduct-delete-code

    def delete(self, transaction_id, book_id, edition_number):
        query = "DELETE FROM TRANSACTION_PRODUCT WHERE ((TRANSACTION_ID = %s) AND (BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (transaction_id, book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

This function takes the primary key of the ``TRANSACTION_PRODUCT`` table,
``transaction_id``, ``book_id``, and ``edition_number``, as an argument.
The function executes the ``DELETE`` query that is written for the
``TRANSACTION_PRODUCT`` table by filling it with ``transaction_id``,
``book_id``, and ``edition_number``.

.. code-block:: python
    :linenos:
    :lineno-start: 30
    :caption: **2.6.4: Transaction Product - Get Row Function** (file: ``table_operations/transaction_product.py``, version: ``d1dcbe9``)
    :name: transactionProduct-getRow-code

    def get_row(self, where_columns=None, where_values=None):
        return self.getRowGeneric("*", where_columns, where_values)

This function uses ``getRowGeneric`` function of baseClass.
See `baseClass <baseClass.html>`__ for more.

.. code-block:: python
    :linenos:
    :lineno-start: 33
    :caption: **2.6.5: Transaction Product - Get Table Function** (file: ``table_operations/transaction_product.py``, version: ``d1dcbe9``)
    :name: transactionProduct-getTable-code

    def get_table(self, where_columns=None, where_values=None):
        return self.getTableGeneric("*", where_columns, where_values)

This function uses ``getTableGeneric`` function of baseClass.
See `baseClass <baseClass.html>`__ for more.

CUSTOMER_ADDRESS Table
----------------------

This table stores customer-address relationships.

Attributes of CUSTOMER_ADDRESS Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+----------------+---------+
| ATTRIBUTE NAME | TYPE    |
+================+=========+
| CUSTOMER_ID    | INTEGER |
+----------------+---------+
| ADDRESS_ID     | INTEGER |
+----------------+---------+

- **PRIMARY KEY:** CUSTOMER_ID + ADDRESS_ID
- **FOREIGN KEY:** ``CUSTOMER_ID`` REFERENCES ``CUSTOMER`` TABLE
- **FOREIGN KEY:** ``ADDRESS_ID`` REFERENCES ``ADDRESS`` TABLE

Code of CUSTOMER_ADDRESS Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:
    :lineno-start: 6
    :caption: **2.7.1: Customer Address - Init Function** (file: ``table_operations/customer_address.py``, version: ``d1dcbe9``)
    :name: customerAddress-init-code

    def __init__(self):
        super().__init__("CUSTOMER_ADDRESS", CustomerAddressObj)

Here in ``__init__`` function, ``Customer_Address`` class initializes
its parent class (``baseClass``) with ``table_name`` = ``CUSTOMER_ADDRESS``
and ``cons`` = ``CustomerAddressObj``.

.. code-block:: python
    :linenos:
    :lineno-start: 9
    :caption: **2.7.2: Customer Address - Insert Function** (file: ``table_operations/customer_address.py``, version: ``d1dcbe9``)
    :name: customerAddress-insert-code

    def add(self, customer_address):
        query = "INSERT INTO CUSTOMER_ADDRESS (CUSTOMER_ID, ADDRESS_ID) VALUES (%s, %s);"
        fill = (customer_address.customer_id, customer_address.address_id)

In ``add`` function, it calls ``insertIntoFlex`` (which is introduced
in `baseClass <baseClass.html#baseclass-insertintoflex>`__ part of
documentation) by giving its columns' names as arguments. This function
adds these column names to an ``INSERT INTO`` SQL statement and returns
this string. After that, it calls ``execute`` function with values that are
given as arguments to this function.
