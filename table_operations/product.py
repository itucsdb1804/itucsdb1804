from table_operations.baseClass import baseClass
from tables import ProductObj, BookObj, BookEditionObj
import psycopg2 as dbapi2


class Product(baseClass):
    def __init__(self):
        super().__init__("PRODUCT", ProductObj)

    def add(self, product):
        query = "INSERT INTO PRODUCT (BOOK_ID, EDITION_NUMBER, REMAINING, ACTUAL_PRICE, NUMBER_OF_SELLS, PRODUCT_EXPLANATION, IS_ACTIVE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        fill = (product.book_id, product.edition_number, product.remaining, product.actual_price, product.number_of_sells, product.explanation, product.is_active)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def update(self, book_id, edition_number, product):
        query = "UPDATE PRODUCT SET REMAINING = %s, ACTUAL_PRICE = %s, NUMBER_OF_SELLS = %s, PRODUCT_EXPLANATION = %s, IS_ACTIVE = %s WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (product.remaining, product.actual_price, product.number_of_sells, product.explanation, product.is_active, book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def delete(self, book_id, edition_number):
        query = "DELETE FROM PRODUCT WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def get_row(self, book_id, edition_number):
        _product = None

        query = "SELECT * FROM PRODUCT WHERE ((BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            product = cursor.fetchone()
            if product is not None:
                _product = ProductObj(product[0], product[1], product[2], product[3], product[4], product[5], product[7], date_added=product[6])

        return _product

    def get_table(self):
        products = []

        query = "SELECT * FROM PRODUCT;"

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            for product in cursor:
                product_ = ProductObj(product[0], product[1], product[2], product[3], product[4], product[5], product[7], date_added=product[6])
                products.append(product_)
            cursor.close()

        return products

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
                print(all_info)
                product_ = ProductObj(all_info[0], all_info[1], all_info[2], all_info[3], all_info[4], all_info[5], all_info[7], date_added=all_info[6])
                book_editions_ = BookEditionObj(all_info[9], all_info[10], all_info[11], all_info[12], all_info[13], all_info[14], all_info[15])
                book_ = BookObj(all_info[17], all_info[18], all_info[19], book_id=all_info[16])
                products_editions_books.append([product_, book_editions_, book_])
            cursor.close()

        return products_editions_books
