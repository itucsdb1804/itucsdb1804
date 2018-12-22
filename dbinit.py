import os
import sys
import psycopg2 as dbapi2


INIT_STATEMENTS = [
    #"DROP SCHEMA public CASCADE;CREATE SCHEMA public;",

    """CREATE TABLE IF NOT EXISTS BOOK (
        BOOK_ID         SERIAL PRIMARY KEY,
        BOOK_NAME       VARCHAR(100),
        RELEASE_YEAR    SMALLINT,
        BOOK_EXPLANATION     VARCHAR(1000)
    )""",

    """
    CREATE TABLE IF NOT EXISTS CATEGORY (
        CATEGORY_ID     SERIAL PRIMARY KEY,
        CATEGORY_NAME   VARCHAR(50) UNIQUE
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
        DATE_OF_BIRTH   DATE,
        NATIONALITY     VARCHAR(50)
    )  """,

    """
    CREATE TABLE IF NOT EXISTS CUSTOMER (
        CUSTOMER_ID     SERIAL PRIMARY KEY,
        PERSON_ID       INTEGER REFERENCES PERSON (PERSON_ID) UNIQUE,
        USERNAME        VARCHAR(20) UNIQUE NOT NULL,
        EMAIL           VARCHAR(50) UNIQUE NOT NULL,
        PASS_HASH       CHAR(87) NOT NULL,
        PHONE           CHAR(10) UNIQUE NOT NULL,
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
        ADDR_NUMBER     VARCHAR(10),
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

    """DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'rate_type') THEN
            CREATE DOMAIN RATE_TYPE AS SMALLINT
            CHECK (
                (VALUE > 0) AND (VALUE <= 5)
            );
        END IF;
    END$$;""",

    """CREATE TABLE IF NOT EXISTS COMMENT (
        COMMENT_ID        SERIAL PRIMARY KEY,
        CUSTOMER_ID       INTEGER REFERENCES CUSTOMER (CUSTOMER_ID),
        BOOK_ID           INTEGER REFERENCES BOOK (BOOK_ID),
        COMMENT_TITLE     VARCHAR(50) NOT NULL,
        COMMENT_STATEMENT VARCHAR(500) NOT NULL,
        ADDED_TIME        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UPDATED_TIME      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        RATING            RATE_TYPE
    )""",

    """CREATE TABLE IF NOT EXISTS CUSTOMER_ADDRESS (
        CUSTOMER_ID     INTEGER REFERENCES CUSTOMER (CUSTOMER_ID),
        ADDRESS_ID      INTEGER REFERENCES ADDRESS (ADDRESS_ID),
        PRIMARY KEY     (CUSTOMER_ID, ADDRESS_ID)
    )""",

    """CREATE TABLE IF NOT EXISTS BOOK_EDITION (
        BOOK_ID         INTEGER REFERENCES BOOK (BOOK_ID),
        EDITION_NUMBER  SMALLINT,
        ISBN            VARCHAR(20),
        PUBLISHER       VARCHAR(100),
        PUBLISH_YEAR    SMALLINT,
        NUMBER_OF_PAGES SMALLINT,
        LANGUAGE        VARCHAR(50),
        PRIMARY KEY     (BOOK_ID, EDITION_NUMBER)
    )""",

    """CREATE TABLE IF NOT EXISTS TRANSACTION (
        TRANSACTION_ID           SERIAL PRIMARY KEY,
        CUSTOMER_ID              INTEGER REFERENCES CUSTOMER (CUSTOMER_ID),
        ADDRESS_ID               INTEGER REFERENCES ADDRESS (ADDRESS_ID) DEFAULT NULL,
        TRANSACTION_TIME         TIMESTAMP DEFAULT NULL,
        PAYMENT_TYPE             VARCHAR(30) DEFAULT NULL,
        TRANSACTION_EXPLANATION  VARCHAR(200) DEFAULT NULL,
        IS_COMPLETED             BOOLEAN DEFAULT FALSE
    )""",

    """CREATE TABLE IF NOT EXISTS PRODUCT (
        BOOK_ID              INTEGER,
        EDITION_NUMBER       SMALLINT,
        REMAINING            SMALLINT NOT NULL DEFAULT 0,
        ACTUAL_PRICE         FLOAT,
        NUMBER_OF_SELLS      SMALLINT DEFAULT 0,
        PRODUCT_DATE_ADDED   DATE NOT NULL DEFAULT CURRENT_DATE,
        PRODUCT_EXPLANATION  VARCHAR(500),
        IS_ACTIVE            BOOLEAN DEFAULT TRUE,
        FOREIGN KEY          (BOOK_ID, EDITION_NUMBER) REFERENCES BOOK_EDITION (BOOK_ID, EDITION_NUMBER),
        PRIMARY KEY          (BOOK_ID, EDITION_NUMBER)
    )""",

    """CREATE TABLE IF NOT EXISTS TRANSACTION_PRODUCT (
        TRANSACTION_ID  INTEGER REFERENCES TRANSACTION (TRANSACTION_ID),
        BOOK_ID         INTEGER,
        EDITION_NUMBER  SMALLINT,
        PIECE           SMALLINT DEFAULT 1,
        UNIT_PRICE      FLOAT,
        FOREIGN KEY     (BOOK_ID, EDITION_NUMBER) REFERENCES PRODUCT (BOOK_ID, EDITION_NUMBER),
        PRIMARY KEY     (TRANSACTION_ID, BOOK_ID, EDITION_NUMBER)
    )""",

    # "INSERT INTO BOOK (BOOK_NAME, RELEASE_YEAR, BOOK_EXPLANATION) VALUES ('Book name 1', 2001, 'Book Explanation 1')",
    # "INSERT INTO BOOK (BOOK_NAME, RELEASE_YEAR, BOOK_EXPLANATION) VALUES ('Book name 2', 2002, 'Book Explanation 2')",
    # "INSERT INTO BOOK (BOOK_NAME, RELEASE_YEAR, BOOK_EXPLANATION) VALUES ('Book name 3', 2003, 'Book Explanation 3')",
    # "INSERT INTO ADDRESS (ADDRESS_NAME, COUNTRY, CITY, DISTRICT, NEIGHBORHOOD, AVENUE, STREET, ADDR_NUMBER, ZIPCODE, EXPLANATION) VALUES ('Address name 1', 'adress __ 1', 'adress __ 1', 'adress __ 1', 'adress __ 1', 'adress __ 1', 'adress __ 1', 1, '35510', 'adress __ 1' )",
    # "INSERT INTO ADDRESS (ADDRESS_NAME, COUNTRY, CITY, DISTRICT, NEIGHBORHOOD, AVENUE, STREET, ADDR_NUMBER, ZIPCODE, EXPLANATION) VALUES ('Address name 2', 'adress __ 2', 'adress __ 2', 'adress __ 2', 'adress __ 2', 'adress __ 2', 'adress __ 2', 2, '35512', 'adress __ 2' )",
    # "INSERT INTO PERSON (PERSON_NAME, SURNAME, GENDER, DATE_OF_BIRTH, NATIONALITY) VALUES ('Ahmet', 'AKBULUT', 'F', '2000-12-20', 'Nationality 1')",
    # "INSERT INTO PERSON (PERSON_NAME, SURNAME, GENDER, DATE_OF_BIRTH, NATIONALITY) VALUES ('Yasin', 'YILMAZ', 'M', '2002-12-20', 'Nationality 2')",
    # "INSERT INTO PERSON (PERSON_NAME, SURNAME, GENDER, DATE_OF_BIRTH, NATIONALITY) VALUES ('Abdullah', 'HATİP', 'M', '2002-12-20', 'Nationality 3')",
    # "INSERT INTO CUSTOMER (PERSON_ID, USERNAME, EMAIL, PASS_HASH, PHONE, IS_ACTIVE) VALUES (1, 'Username 1', 'email1@itu.edu.tr', '$pbkdf2-sha256$29000$FwIg5HzPGQNA6F2L8T6n9A$pEuXZzioC9cmHF.O/cst5/.it8QmT1Z9JEJn5PsGHWE', '2325421326', TRUE)",
    # "INSERT INTO CUSTOMER (PERSON_ID, USERNAME, EMAIL, PASS_HASH, PHONE, IS_ACTIVE) VALUES (2, 'Username 2', 'email2@itu.edu.tr', '$pbkdf2-sha256$29000$FwIg5HzPGQNA6F2L8T6n9A$pEuXZzioC9cmHF.O/cst5/.it8QmT1Z9JEJn5PsGHWE', '2325428326', FALSE)",
    # "INSERT INTO COMMENT (CUSTOMER_ID, BOOK_ID, COMMENT_TITLE, COMMENT_STATEMENT, ADDED_TIME, UPDATED_TIME, RATING) VALUES (1, 1, 'Comment title 1', 'comment statement  statement 1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)",
    # "INSERT INTO COMMENT (CUSTOMER_ID, BOOK_ID, COMMENT_TITLE, COMMENT_STATEMENT, ADDED_TIME, UPDATED_TIME, RATING) VALUES (2, 2, 'Comment title 2', 'comment statement  statement 2', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 2)",
    # # "INSERT INTO BOOK_EDITION (BOOK_ID, EDITION_NUMBER, ISBN, PUBLISHER, PUBLISH_YEAR, NUMBER_OF_PAGES, LANGUAGE) VALUES (BOOK_ID, EDITION_NUMBER, ISBN, PUBLISHER, PUBLISH_YEAR, NUMBER_OF_PAGES, LANGUAGE)",
    # "INSERT INTO BOOK_EDITION (BOOK_ID, EDITION_NUMBER, ISBN, PUBLISHER, PUBLISH_YEAR, NUMBER_OF_PAGES, LANGUAGE) VALUES (1, 1, '123456789', 'publisher A', 2000, 211, 'Türkçe')",
    # "INSERT INTO BOOK_EDITION (BOOK_ID, EDITION_NUMBER, ISBN, PUBLISHER, PUBLISH_YEAR, NUMBER_OF_PAGES, LANGUAGE) VALUES (1, 2, '223456789', 'publisher B', 2000, 211, 'Türkçe')",
    # "INSERT INTO BOOK_EDITION (BOOK_ID, EDITION_NUMBER, ISBN, PUBLISHER, PUBLISH_YEAR, NUMBER_OF_PAGES, LANGUAGE) VALUES (1, 3, '323456789', 'publisher B', 2000, 211, 'Türkçe')",
    # "INSERT INTO BOOK_EDITION (BOOK_ID, EDITION_NUMBER, ISBN, PUBLISHER, PUBLISH_YEAR, NUMBER_OF_PAGES, LANGUAGE) VALUES (2, 1, '423456789', 'publisher A', 2000, 211, 'Türkçe')",
    # "INSERT INTO BOOK_EDITION (BOOK_ID, EDITION_NUMBER, ISBN, PUBLISHER, PUBLISH_YEAR, NUMBER_OF_PAGES, LANGUAGE) VALUES (2, 2, '523456789', 'publisher A', 2000, 211, 'Türkçe')",
    # # "INSERT INTO PRODUCT (BOOK_ID, EDITION_NUMBER, REMAINING, ACTUAL_PRICE, NUMBER_OF_SELLS, PRODUCT_DATE_ADDED, PRODUCT_EXPLANATION, IS_ACTIVE) VALUES (BOOK_ID, EDITION_NUMBER, REMAINING, ACTUAL_PRICE, NUMBER_OF_SELLS, PRODUCT_DATE_ADDED, PRODUCT_EXPLANATION, IS_ACTIVE)",
    # "INSERT INTO PRODUCT (BOOK_ID, EDITION_NUMBER, REMAINING, ACTUAL_PRICE, NUMBER_OF_SELLS, PRODUCT_DATE_ADDED, PRODUCT_EXPLANATION, IS_ACTIVE) VALUES (1, 1, 999, 3, 999, '2018-12-25', 'Product explanation 1', TRUE)",
    # "INSERT INTO PRODUCT (BOOK_ID, EDITION_NUMBER, REMAINING, ACTUAL_PRICE, NUMBER_OF_SELLS, PRODUCT_DATE_ADDED, PRODUCT_EXPLANATION, IS_ACTIVE) VALUES (1, 2, 999, 4, 999, '2018-12-25', 'Product explanation 1', TRUE)",
    # "INSERT INTO PRODUCT (BOOK_ID, EDITION_NUMBER, REMAINING, ACTUAL_PRICE, NUMBER_OF_SELLS, PRODUCT_DATE_ADDED, PRODUCT_EXPLANATION, IS_ACTIVE) VALUES (1, 3, 999, 5, 999, '2018-12-25', 'Product explanation 1', FALSE)",
    # "INSERT INTO PRODUCT (BOOK_ID, EDITION_NUMBER, REMAINING, ACTUAL_PRICE, NUMBER_OF_SELLS, PRODUCT_DATE_ADDED, PRODUCT_EXPLANATION, IS_ACTIVE) VALUES (2, 1, 999, 6, 999, '2018-12-25', 'Product explanation 1', FALSE)",
    # "INSERT INTO PRODUCT (BOOK_ID, EDITION_NUMBER, REMAINING, ACTUAL_PRICE, NUMBER_OF_SELLS, PRODUCT_DATE_ADDED, PRODUCT_EXPLANATION, IS_ACTIVE) VALUES (2, 2, 999, 7, 999, '2018-12-25', 'Product explanation 1', TRUE)",
    # "INSERT INTO AUTHOR (PERSON_ID, BIOGRAPHY) VALUES (1, 'biografy example 1')",
    # "INSERT INTO AUTHOR (PERSON_ID, BIOGRAPHY) VALUES (2, 'biografy example 2')",
    # "INSERT INTO AUTHOR (PERSON_ID, BIOGRAPHY) VALUES (3, 'biografy example 3')",
    # # "INSERT INTO TRANSACTION (CUSTOMER_ID) VALUES (CUSTOMER_ID)",
    # "INSERT INTO TRANSACTION (CUSTOMER_ID) VALUES (1)",
    # "INSERT INTO TRANSACTION (CUSTOMER_ID) VALUES (2)",
    # # "INSERT INTO BOOK_AUTHOR (BOOK_ID, AUTHOR_ID) VALUES (BOOK_ID, AUTHOR_ID)",
    # "INSERT INTO BOOK_AUTHOR (BOOK_ID, AUTHOR_ID) VALUES (1, 1)",
    # "INSERT INTO BOOK_AUTHOR (BOOK_ID, AUTHOR_ID) VALUES (1, 2)",
    # "INSERT INTO BOOK_AUTHOR (BOOK_ID, AUTHOR_ID) VALUES (1, 3)",
    # "INSERT INTO BOOK_AUTHOR (BOOK_ID, AUTHOR_ID) VALUES (2, 3)",
    # "INSERT INTO BOOK_AUTHOR (BOOK_ID, AUTHOR_ID) VALUES (3, 2)",
    # "INSERT INTO BOOK_AUTHOR (BOOK_ID, AUTHOR_ID) VALUES (3, 1)",
    # # "INSERT INTO CATEGORY (CATEGORY_NAME) VALUES (CATEGORY_NAME)",
    # "INSERT INTO CATEGORY (CATEGORY_NAME) VALUES ('Hikaye')",
    # "INSERT INTO CATEGORY (CATEGORY_NAME) VALUES ('Roman')",
    # "INSERT INTO CATEGORY (CATEGORY_NAME) VALUES ('Deneme')",
    # "INSERT INTO CATEGORY (CATEGORY_NAME) VALUES ('Korku')",
    # "INSERT INTO CATEGORY (CATEGORY_NAME) VALUES ('Macera')",
    # "INSERT INTO CATEGORY (CATEGORY_NAME) VALUES ('Korku')",
    # "INSERT INTO CATEGORY (CATEGORY_NAME) VALUES ('Epik')",
    # # "INSERT INTO CUSTOMER_ADDRESS (CUSTOMER_ID, ADDRESS_ID) VALUES (CUSTOMER_ID, ADDRESS_ID)",
    # "INSERT INTO CUSTOMER_ADDRESS (CUSTOMER_ID, ADDRESS_ID) VALUES (1, 1)",
    # "INSERT INTO CUSTOMER_ADDRESS (CUSTOMER_ID, ADDRESS_ID) VALUES (1, 2)",
]

GENRES = ["Art", "Biography", "Business", "Children", "Classics", "Comics", "Contemporary", "Cookbooks", "Crime", "Fantasy", "Fiction", "History", "Horror", "Humor and Comedy", "Music", "Mystery", "Nonfiction", "Philosophy", "Poetry", "Psychology", "Religion", "Romance", "Science", "Science Fiction", "Sports", "Thriller", "Travel", "Other"]
GEN_INSERT = "INSERT INTO CATEGORY (CATEGORY_NAME) VALUES (%s)"

def initialize(url2):
    with dbapi2.connect(url2) as connection:
        with connection.cursor() as cursor:
            for statement in INIT_STATEMENTS:
                print("SQL Run:", statement)
                cursor.execute(statement)
            for gen in GENRES:              # To insert initial genres
                try:
                    cursor.execute(GEN_INSERT, (gen, ))
                except dbapi2.DatabaseError: # as err:
                    #print("Warning: ", err)
                    pass


if __name__ == "__main__":

    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
