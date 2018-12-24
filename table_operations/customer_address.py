from table_operations.baseClass import baseClass
from tables import CustomerAddressObj


class CustomerAddress(baseClass):
    def __init__(self):
        super().__init__("CUSTOMER_ADDRESS", CustomerAddressObj)

    def add(self, customer_address):
        query = "INSERT INTO CUSTOMER_ADDRESS (CUSTOMER_ID, ADDRESS_ID) VALUES (%s, %s);"
        fill = (customer_address.customer_id, customer_address.address_id)
        self.execute(query, fill)
