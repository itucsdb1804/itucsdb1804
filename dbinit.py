import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    # myilmaz
    """CREATE TABLE IF NOT EXISTS BOOK (
        BOOK_ID         SERIAL PRIMARY KEY,
        BOOK_NAME       VARCHAR(100),
        RELEASE_YEAR    SMALLINT,
        EXPLANATION     VARCHAR(1000)
    )""",

    """
    CREATE TABLE IF NOT EXISTS CATEGORY (
        CATEGORY_ID     SERIAL PRIMARY KEY,
        CATEGORY_NAME   VARCHAR(50)
    )  """,

    """
    CREATE TABLE IF NOT EXISTS BOOK_CATEGORY (
        BOOK_ID         INTEGER REFERENCES BOOK (BOOK_ID),
        CATEGORY_ID     INTEGER REFERENCES CATEGORY (CATEGORY_ID),
        PRIMARY KEY     (BOOK_ID, CATEGORY_ID)
    )  """,

    """
    DROP TYPE IF EXISTS GENDER_TYPE;
    CREATE DOMAIN GENDER_TYPE AS CHAR(1)
    CHECK (
        (VALUE = 'F') OR (VALUE = 'M') OR (VALUE = 'O')
    )  """,

    """
    CREATE TABLE IF NOT EXISTS PERSON (
        PERSON_ID       SERIAL PRIMARY KEY,
        PERSON_NAME     VARCHAR(50) NOT NULL,
        SURNAME         VARCHAR(50) NOT NULL,
        GENDER          GENDER_TYPE,
        DATE_OF_BIRTH   DATE NOT NULL,
        NATIONALITY     VARCHAR(50)
    )  """,

    """
    CREATE TABLE IF NOT EXISTS CUSTOMER (
        CUSTOMER_ID     SERIAL PRIMARY KEY,
        PERSON_ID       INTEGER REFERENCES PERSON (PERSON_ID) UNIQUE,
        USERNAME        VARCHAR(20) UNIQUE NOT NULL,
        EMAIL           VARCHAR(50) UNIQUE NOT NULL,
        PASS_HASH       CHAR(44) NOT NULL,
        PERSON_PHONE    CHAR(10) UNIQUE NOT NULL,
        IS_ACTIVE       BOOLEAN DEFAULT TRUE
    )  """,

    """
    CREATE TABLE IF NOT EXISTS ADDRESS (
        ADDRESS_ID      SERIAL PRIMARY KEY,
        ADDRESS_NAME    VARCHAR(30),
        COUNTRY         VARCHAR(30) NOT NULL,
        CITY            VARCHAR(30) NOT NULL,
        DISTRICT        VARCHAR(30),
        NEIGHBORHOOD    VARCHAR(30),
        AVENUE          VARCHAR(30),
        STREET          VARCHAR(30),
        NUMBER          VARCHAR(10),
        ZIPCODE         CHAR(5),
        EXPLANATION     VARCHAR(500)
    )  """,

    """
    CREATE TABLE IF NOT EXISTS AUTHOR (
        AUTHOR_ID       SERIAL PRIMARY KEY,
        PERSON_ID       INTEGER REFERENCES PERSON (PERSON_ID),
        BIOGRAPHY       VARCHAR(1000)
    )  """,

    """
    CREATE TABLE IF NOT EXISTS BOOK_AUTHOR (
        BOOK_ID         INTEGER REFERENCES BOOK (BOOK_ID),
        AUTHOR_ID       INTEGER REFERENCES AUTHOR (AUTHOR_ID),
        PRIMARY KEY     (BOOK_ID, AUTHOR_ID)
    )  """
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
    