import psycopg2 as dbapi2
from table_operations.baseClass import baseClass
from tables import TransactionObj


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

    def add_empty(self, customer_id):
        query = "INSERT INTO TRANSACTION (CUSTOMER_ID) VALUES (%s)"
        fill = (customer_id,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def update(self, update_columns, new_values, where_columns, where_values):
        self.updateGeneric(update_columns, new_values, where_columns, where_values)

    def delete(self, transaction_key):
        query = "DELETE FROM TRANSACTION WHERE TRANSACTION_ID = %s"
        fill = (transaction_key,)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def get_row(self, select_columns="*", where_columns=None, where_values=None):
        return self.getRowGeneric(select_columns, where_columns, where_values)

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
