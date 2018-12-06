from table_operations.baseClass import baseClass
from tables import StoreObj
import psycopg2 as dbapi2

class Store(baseClass):
    def __init__(self):
        super().__init__("STORE", StoreObj)

    def add(self, store):
        query = "INSERT INTO STORE (STORE_NAME, STORE_PHONE, ADDRESS_ID, STORE_EMAIL, WEBSITE, STORE_DATE_ADDED, STORE_EXPLANATION) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        fill = (store.store_name, store.store_phone, store.address_id, store.email, store.website, store.date_added, store.explanation)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def update(self, store_key, store):
        query = "UPDATE BOOK SET STORE_NAME = %s, STORE_PHONE = %s, ADDRESS_ID = %s, STORE_EMAIL = %s, STORE_WEBSITE = %s, STORE_DATE_ADDED = %s, EXPLANATION = %s WHERE STORE_ID = %s"
        fill = (store.store_name, store.store_phone, store.address_id, store.email, store.website, store.date_added, store.explanation, store_key)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def delete(self, store_key):
        query = "DELETE FROM STORE WHERE STORE_ID = %s"
        fill = (store_key)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def get_row(self, store_key):
        _store = None

        query = "SELECT * FROM STORE WHERE STORE_ID = %s"
        fill = (store_key)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            store = cursor.fetchone()
            if store is not None:
                _store = StoreObj(store[1], store[2], store[3], store[4], store[5], store[6], store[7])

        return _store

    def get_table(self):
        stores = []

        query = "SELECT * FROM STORE;"

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            for store in cursor:
                store_ = StoreObj(store[1], store[2], store[3], store[4], store[5], store[6], store[7])
                stores.append((store[0], store_))
            cursor.close()

        return stores
