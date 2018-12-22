Developer Guide
===============

Database Design
---------------

**explain the database design of your project**

**include the E/R diagram(s)**

Code
----

**explain the technical structure of your code**

**to include a code listing, use the following example**

.. code-block

.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :caption: baseClass
   :name: Base Class
   :lines: 1-14


.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 16
   :caption: baseClass deleteGeneric
   :name: Base Class deleteGeneric
   :lines: 16-21

.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 23
   :caption: baseClass updateGeneric
   :name: Base Class updateGeneric
   :lines: 23-30

.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 32
   :caption: baseClass getRowGeneric
   :name: Base Class getRowGeneric
   :lines: 32-48

.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 50
   :caption: baseClass getTableGeneric
   :name: Base Class getTableGeneric
   :lines: 50-68



.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 93
   :caption: baseClass execute
   :name: Base Class execute
   :lines: 93-105

.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 108
   :caption: baseClass whereFlex
   :name: Base Class whereFlex
   :lines: 108-112



.. literalinclude:: /../../table_operations/baseClass.py
   :language: python
   :linenos:
   :lineno-start: 115
   :caption: baseClass convertToList
   :name: Base Class convertToList
   :lines: 115-120

This piece of code takes an argument and
checks the type of the argument whether it is list or not.
If it is not an instance of type list,
it converts this argument to a list and returns it.
Else, it returns the argument directly.


.. toctree::

   member1
   member2
