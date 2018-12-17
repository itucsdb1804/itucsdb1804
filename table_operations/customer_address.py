from table_operations.baseClass import baseClass
from tables import CustomerAddressObj


class CustomerAddress(baseClass):
    def __init__(self):
        super().__init__("CUSTOMER_ADDRESS", CustomerAddressObj)

    def add(self, customer_address):
        query = "INSERT INTO CUSTOMER_ADDRESS (CUSTOMER_ID, ADDRESS_ID) VALUES (%s, %s);"
        fill = (customer_address.customer_id, customer_address.address_id)
        self.execute(query, fill)

    def update(self, update_columns, new_values, where_columns, where_values):
        self.updateGeneric(update_columns, new_values, where_columns, where_values)

    def delete(self, where_values, where_columns="ADDRESS_ID"):
        self.deleteGeneric(where_columns, where_values)

    def get_row(self, where_columns=None, where_values=None):
        return self.getRowGeneric("*", where_columns, where_values)

    def get_table(self, where_columns=None, where_values=None):
        return self.getTableGeneric("*", where_columns, where_values)
