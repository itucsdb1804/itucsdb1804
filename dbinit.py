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
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'gender_type') THEN
            CREATE DOMAIN GENDER_TYPE AS CHAR(1)
            CHECK (
                (VALUE = 'F') OR (VALUE = 'M') OR (VALUE = 'O')
            );
        END IF;
    END$$;  """,

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
    )  """,
    
    # myilmaz
    """CREATE TABLE IF NOT EXISTS STORE (
        STORE_ID        SERIAL PRIMARY KEY,
        STORE_NAME      VARCHAR(100) NOT NULL,
        STORE_PHONE     CHAR(15) UNIQUE NOT NULL,
        ADDRESS_ID      INTEGER REFERENCES ADDRESS (ADDRESS_ID),
        EMAIL           VARCHAR(50) UNIQUE NOT NULL,
        WEBSITE         VARCHAR(50) UNIQUE,
        DATE_ADDED      DATE NOT NULL DEFAULT CURRENT_DATE,
        EXPLANATION     VARCHAR(1000)
    )""",

    """DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'rate_type') THEN
            CREATE DOMAIN RATE_TYPE AS SMALLINT
            CHECK (
                (VALUE >= 0) AND (VALUE <= 5)
            );
        END IF;
    END$$;""",

    # myilmaz
    """CREATE TABLE IF NOT EXISTS COMMENT (
        COMMENT_ID        SERIAL PRIMARY KEY,
        CUSTOMER_ID       INTEGER REFERENCES CUSTOMER (CUSTOMER_ID),
        BOOK_ID           INTEGER REFERENCES BOOK (BOOK_ID),
        COMMENT_TITLE     VARCHAR(50) NOT NULL,
        COMMENT_STATEMENT VARCHAR(500) NOT NULL,
        ADDED_TIME        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UPDATED_TIME      TIMESTAMP DEFAULT NULL,
        RATING            RATE_TYPE
    )""",

    # myilmaz
    """CREATE TABLE IF NOT EXISTS CUSTOMER_ADDRESS (
        CUSTOMER_ID     INTEGER REFERENCES CUSTOMER (CUSTOMER_ID),
        ADDRESS_ID      INTEGER REFERENCES ADDRESS (ADDRESS_ID),
        PRIMARY KEY     (CUSTOMER_ID, ADDRESS_ID)
    )""",

    # myilmaz
    """CREATE TABLE IF NOT EXISTS BOOK_EDITION (
        BOOK_ID         INTEGER REFERENCES BOOK (BOOK_ID),
        EDITION_NUMBER  SMALLINT,
        ISBN            INTEGER UNIQUE,
        PUBLISHER       VARCHAR(100),
        PUBLISH_YEAR    SMALLINT,
        NUMBER_OF_PAGES SMALLINT,
        LANGUAGE        VARCHAR(50),
        PRIMARY KEY     (BOOK_ID, EDITION_NUMBER)
    )""",
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
    