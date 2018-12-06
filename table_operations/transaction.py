from table_operations.baseClass import baseClass
from tables import TransactionObj
import psycopg2 as dbapi2

class Transaction(baseClass):
    def __init__(self):
        super().__init__("TRANSACTION", TransactionObj)

    def add(self, transaction):
        query = "INSERT INTO TRANSACTION (CUSTOMER_ID, ADDRESS_ID, TRANSACTION_TIME, PAYMENT_TYPE, TRANSACTION_EXPLANATION) VALUES (%s, %s, %s, %s, %s)"
        fill = (transaction.customer_id, transaction.address_id, transaction.transaction_time, transaction.payment_type, transaction.explanation)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def update(self, transaction_key, transaction):
        query = "UPDATE TRANSACTION SET CUSTOMER_ID = %s, ADDRESS_ID = %s, TRANSACTION_TIME = %s, PAYMENT_TYPE = %s, TRANSACTION_EXPLANATION = %s WHERE TRANSACTION_ID = %s"
        fill = (transaction.customer_id, transaction.address_id, transaction.transaction_time, transaction.payment_type, transaction.explanation, transaction_key)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def delete(self, transaction_key):
        query = "DELETE FROM TRANSACTION WHERE TRANSACTION_ID = %s"
        fill = (transaction_key)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def get_row(self, transaction_key):
        _transaction = None

        query = "SELECT * FROM TRANSACTION WHERE TRANSACTION_ID = %s"
        fill = (transaction_key)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            transaction = cursor.fetchone()
            if transaction is not None:
                _transaction = TransactionObj(transaction[1], transaction[2], transaction[3], transaction[4], transaction[5])

        return _transaction

    def get_table(self):
        transactions = []

        query = "SELECT * FROM TRANSACTION;"

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            for transaction in cursor:
                transaction_ = TransactionObj(transaction[1], transaction[2], transaction[3], transaction[4], transaction[5])
                transactions.append((transaction[0], transaction_))
            cursor.close()

        return transactions
