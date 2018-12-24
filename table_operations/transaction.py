import psycopg2 as dbapi2
from table_operations.baseClass import baseClass
from tables import TransactionObj


class Transaction(baseClass):
    def __init__(self):
        super().__init__("TRANSACTION", TransactionObj)

    def add(self, transaction):
        query = "INSERT INTO TRANSACTION (CUSTOMER_ID, ADDRESS_ID, TRANSACTION_TIME, PAYMENT_TYPE, TRANSACTION_EXPLANATION) VALUES (%s, %s, %s, %s, %s)"
        fill = (transaction.customer_id, transaction.address_id, transaction.transaction_time, transaction.payment_type, transaction.explanation)

        self.execute(query, fill)

    def add_empty(self, customer_id):
        query = "INSERT INTO TRANSACTION (CUSTOMER_ID) VALUES (%s)"
        fill = (customer_id, )

        self.execute(query, fill)

    def delete(self, transaction_key):
        query = "DELETE FROM TRANSACTION WHERE TRANSACTION_ID = %s"
        fill = (transaction_key, )

        self.execute(query, fill)

    def get_row(self, select_columns="*", where_columns=None, where_values=None):
        return self.getRowGeneric(select_columns, where_columns, where_values)

    def get_table(self):
        return self.getTableGeneric("*")
