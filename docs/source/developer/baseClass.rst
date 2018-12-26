.. role:: sql(code)
   :language: sql
   :class: highlight


baseClass
=========


Code
----

**Here is the code and explanation for base class:**


.. code-block

.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :caption: baseClass init
   :name: baseClass init
   :lines: 1-14


In initialization part of ``baseClass``, tablename attribute holds
the name of the derived table from ``baseClass``. ``cons`` attribute
is to hold constructor of this table while its instances are
converted from SQL records to the object. ``url`` variable is to
take the link of database connection.


.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 17
   :caption: baseClass deleteGeneric
   :name: baseClass deleteGeneric
   :lines: 17-22

``deleteGeneric`` function takes 2 parameters to determine which
data will be deleted. ``where_columns`` argument of this function
is to select from these attributes and ``where_values`` argument is
for filtering results. This function works as generic for all classes
that are derived from ``baseClass``.

.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 25
   :caption: baseClass update
   :name: baseClass update
   :lines: 25-32

``update`` function takes 4 parameters to determine which
data will be deleted. ``where_columns`` argument of this function
is to select from these attributes and ``where_values`` argument is
for filtering results. ``update_columns`` argument of this function is
to determine which columns of this table will be updated and ``new_values``
argument is for the new values of this columns.
This function is available for all classes that are derived from
``baseClass``, so it works as generic.

.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 35
   :caption: baseClass get_row
   :name: baseClass get_row
   :lines: 35-47

``get_row`` function is to take one result from a table.
``select_columns`` arguments shows the columns that will be returned and
``where_columns`` and ``where_values`` arguments are to filter the results
according to given arguments. This function works as generic for all
classes that are derived from ``baseClass``.

.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 50
   :caption: baseClass get_table
   :name: baseClass get_table
   :lines: 50-67

``get_table`` function is to take more than one results from a table.
``select_columns`` arguments shows the columns that will be returned and
``where_columns`` and ``where_values`` arguments are to filter the results
according to given arguments. This function works as generic for all
classes that are derived from ``baseClass``.

.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 77
   :caption: baseClass execute
   :name: baseClass execute
   :lines: 77-89

This ``execute`` function takes three arguments (``query``, ``fill``,
``fetch_bool``). ``query`` argument is the string that will be filled
with values (``fill``) argument. ``fetch_bool`` argument is to
determine whether this query is a fetch query or not and according to
its value, after the query is executed, fetch operation is run to take
results from database.

.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 70
   :caption: baseClass insertIntoFlex
   :name: baseClass insertIntoFlex
   :lines: 70-74

This function takes only ``insert_columns`` arguments which are the columns
of the table (that is derived from ``baseClass``) and place them to appropriate
positions in a ``INSERT INTO`` statement. Then returns this statement (string)
and corresponding empty value fields (to be filled by execute command).

===============================================================================


*There are other functions which are available for use of baseClass but not
directly a method of baseClass:*


.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 94
   :caption: baseClass deleteFlex
   :name: baseClass deleteFlex
   :lines: 94-95

This function takes two arguments (``tablename``, ``where_columns``) and
adds these column name strings and corresponding empty value fields
(to be filled by execute command) to a :sql:`DELETE` query. Then returns this
statement (string) by adding tablename to appropriate position also.

.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 98
   :caption: baseClass updateFlex
   :name: baseClass updateFlex
   :lines: 98-100

This function takes three arguments (``tablename``, ``update_columns``,
``where_columns``) and adds these column name strings (``update_columns``
and ``where_columns``) and corresponding empty value fields for
``where_columns`` (to be filled by execute command) to a :sql:`UPDATE` query.
Then returns this statement (string) by adding tablename to appropriate
position also.

.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 103
   :caption: baseClass getFlex
   :name: baseClass getFlex
   :lines: 103-105

This function takes three arguments (``tablename``, ``select_columns``,
``where_columns``) and adds these column name strings (``select_columns``
and ``where_columns``) and corresponding empty value fields for
``where_columns`` (to be filled by execute command) to a :sql:`SELECT` query.
Then returns this statement (string) by adding tablename to appropriate
position also. This function is used by both of ``getRowGeneric`` and
``getTableGeneric`` functions on their operations.


.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 108
   :caption: baseClass whereFlex
   :name: baseClass whereFlex
   :lines: 108-112

This function takes two arguments (``tablename``, ``where_columns``) and
adds these column name strings and corresponding empty value fields
(to be filled by execute command) to a :sql:`WHERE` query. Then returns this
statement (string) by adding tablename to appropriate position also.


.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 115
   :caption: baseClass convertToList
   :name: baseClass convertToList
   :lines: 115-119

This piece of code takes an argument and
checks the type of the argument whether it is ``list`` or not.
If it is not an instance of type ``list``,
it converts this argument to a ``list`` and returns it.
Else, it returns the argument directly.
