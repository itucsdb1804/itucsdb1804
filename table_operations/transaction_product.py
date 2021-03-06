import psycopg2 as dbapi2
from table_operations.baseClass import baseClass
from tables import TransactionProductObj


class TransactionProduct(baseClass):
    def __init__(self):
        super().__init__("TRANSACTION_PRODUCT", TransactionProductObj)

    def add(self, transaction_product):
        query = "INSERT INTO TRANSACTION_PRODUCT (TRANSACTION_ID, BOOK_ID, EDITION_NUMBER, PIECE, UNIT_PRICE) VALUES (%s, %s, %s, %s, %s)"
        fill = (transaction_product.transaction_id, transaction_product.book_id, transaction_product.edition_number, transaction_product.piece, transaction_product.unit_price)
        self.execute(query, fill)

    def delete(self, transaction_id, book_id, edition_number):
        query = "DELETE FROM TRANSACTION_PRODUCT WHERE ((TRANSACTION_ID = %s) AND (BOOK_ID = %s) AND (EDITION_NUMBER = %s))"
        fill = (transaction_id, book_id, edition_number)
        self.execute(query, fill)
