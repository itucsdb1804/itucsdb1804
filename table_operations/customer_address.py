from table_operations.baseClass import baseClass
from tables import CustomerAddressObj
import psycopg2 as dbapi2

class CustomerAddress(baseClass):
    def __init__(self):
        super().__init__("CUSTOMER_ADDRESS", CustomerAddressObj)

    def add(self, customer_address):
        query = "INSERT INTO CUSTOMER_ADDRESS (CUSTOMER_ID, ADDRESS_ID) VALUES (%s, %s)"
        fill = (customer_address.customer_id, customer_address.address_id)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    def update(self, old_customer_address, updated_customer_address):  # Update address id by customer_id and adress_id

        query = "UPDATE CUSTOMER_ADDRESS SET ADDRESS_ID = %s ((CUSTOMER_ID = %s) AND (ADDRESS_ID = %s))"
        fill = (updated_customer_address.address_id, old_customer_address.customer_id, old_customer_address.address_id)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    # TODO delete all address of a customer, using "customer_address.address_id = none"
    def delete(self, customer_address):
        query = "DELETE FROM CUSTOMER_ADDRESS WHERE ((CUSTOMER_ID = %s) AND (ADDRESS_ID = %s))"
        fill = (customer_address.customer_id, customer_address.address_id)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            cursor.close()

    # TODO None olmayanlara göre seçme yap
    def get_address_ids_by_customer_id(self, customer_id):
        _address_ids = []

        # TODO acaba "SELECT ADDRESS_ID" olur mu?
        query = "SELECT * FROM CUSTOMER_ADDRESS WHERE (CUSTOMER_ID = %s)"
        fill = (customer_id)

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query, fill)
            for customer_address in cursor:
                _address_ids.append(customer_address[1])

        return _address_ids

    def get_table(self):
        customer_addresses = []

        query = "SELECT * FROM CUSTOMER_ADDRESS;"

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            for customer_address in cursor:
                customer_address_ = CustomerAddressObj(customer_address[0], customer_address[1])
                customer_address.append(customer_address_)
            cursor.close()

        return customer_addresses
