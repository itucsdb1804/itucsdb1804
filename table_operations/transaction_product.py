from table_operations.baseClass import baseClass
from tables import TransactionProductObj
import psycopg2 as dbapi2


class TransactionProduct(baseClass):
    def __init__(self):
        super().__init__("TRANSACTION_PRODUCT", TransactionProductObj)

    def add(self, transaction_product):
        query = "INSERT INTO TRANSACTION_PRODUCT (TRANSACTION_ID, BOOK_ID, EDITION_NUMBER, PIECE, UNIT_PRICE) VALUES (%s, %s, %s, %s, %s)"
        fill = (transaction_product.transaction_id, transaction_product.book_id, transaction_product.edition_number, transaction_product.piece, transaction_product.unit_price)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)

    def update(self, update_columns, new_values, where_columns, where_values):
        self.updateGeneric(update_columns, new_values, where_columns, where_values)

    def delete(self, transaction_id, book_id, edition_number):
        query = "DELETE FROM TRANSACTION_PRODUCT WHERE ((TRANSACTION_ID = %s) AND (BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (transaction_id, book_id, edition_number)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def get_row(self, where_columns=None, where_values=None):
        return self.getRowGeneric("*", where_columns, where_values)

    def get_table(self, where_columns=None, where_values=None):
        return self.getTableGeneric("*", where_columns, where_values)
