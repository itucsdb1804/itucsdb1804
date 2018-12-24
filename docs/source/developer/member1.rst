.. include:: <isonum.txt>

Parts Implemented by Ahmed Yasin KUL
=====================================


Person Table
------------


Attributes of Person Table
^^^^^^^^^^^^^^^^^^^^^^^^^^

* PERSON_ID
    - *Type:* SERIAL PRIMARY KEY
    - *Explanation:* Primary key of person object.
* PERSON_NAME
    - *Type:* VARCHAR(50) NOT NULL
    - *Explanation:* Name of the person.
* SURNAME
    - *Type:* VARCHAR(50) NOT NULL
    - *Explanation:* Surname of the person.
* GENDER
    - *Type:* GENDER_TYPE
    - *Explanation:* Gender of the person.
    - *Explanation about type:* It's type is a created domain which accepts
      only one of these three characters:

    =========  ======  =============
    Value: F   |rarr|  Female
    Value: M   |rarr|  Male
    Value: O   |rarr|  Not Specified
    =========  ======  =============


* DATE_OF_BIRTH
    - *Type:* DATE
    - *Explanation:* Date of birth of the person.
* NATIONALITY
    - *Type:* VARCHAR(50)
    - *Explanation:* Nationality of the person.


Code of Person Table
^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: /../../table_operations/person.py
   :language: python
   :linenos:
   :caption: Person Class
   :name: Person Class
   :lines: 1-16




Customer Table
--------------

