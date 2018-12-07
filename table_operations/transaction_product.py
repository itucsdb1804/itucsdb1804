from table_operations.baseClass import baseClass
from tables import TransactionProductObj
import psycopg2 as dbapi2

class TransactionProduct(baseClass):
    def __init__(self):
        super().__init__("TRANSACTION_PRODUCT", TransactionProductObj)

    def add(self, transaction_product):
        query = "INSERT INTO TRANSACTION_PRODUCT (TRANSACTION_ID, BOOK_ID, EDITION_NUMBER, PIECE, UNIT_PRICE) VALUES (%s, %s, %s, %s, %s, %s)"
        fill = (transaction_product.transaction_id, transaction_product.book_id, transaction_product.edition_number, transaction_product.piece, transaction_product.unit_price)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def update(self, transaction_id, book_id, edition_number, transaction_product):
        query = "UPDATE TRANSACTION_PRODUCT SET PIECE = %s, UNIT_PRICE = %s WHERE ((TRANSACTION_ID = %s) AND (BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (transaction_product.piece, transaction_product.unit_price, transaction_id, book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def delete(self, transaction_id, book_id, edition_number):
        query = "DELETE FROM TRANSACTION_PRODUCT WHERE ((TRANSACTION_ID = %s) AND (BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (transaction_id, book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def get_row(self, transaction_id, book_id, edition_number):
        _transaction_product = None

        query = "SELECT * FROM TRANSACTION_PRODUCT WHERE ((TRANSACTION_ID = %s) AND (BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (transaction_id, book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            transaction_product = cursor.fetchone()
            if transaction_product is not None:
                _transaction_product = TransactionProductObj(transaction_product[0], transaction_product[1], transaction_product[2], transaction_product[3], transaction_product[4])

        return _transaction_product

    def get_table(self):
        transaction_product_table = []

        query = "SELECT * FROM BOOK_EDITION;"

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            for transaction_product in cursor:
                transaction_product_ = TransactionProductObj(transaction_product[0], transaction_product[1], transaction_product[2], transaction_product[3], transaction_product[4])
                transaction_product_table.append(transaction_product_)
            cursor.close()

        return transaction_product_table
