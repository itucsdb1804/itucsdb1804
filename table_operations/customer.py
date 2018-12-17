from table_operations.baseClass import baseClass
from tables import CustomerObj

class Customer(baseClass):
    def __init__(self):
        super().__init__("CUSTOMER", CustomerObj)

    def add(self, *values):
        '''
        @param person_id, username, email, password_hash, phone, active
        '''
        assert len(values) == 6
        query = self.insertIntoFlex("PERSON_ID", "USERNAME", "EMAIL", "PASS_HASH", "PHONE", "IS_ACTIVE") + " RETURNING CUSTOMER_ID"
        fill = (*values, )
        last_customer_id = (self.execute(query, fill, True))[0][0]
        return last_customer_id if last_customer_id is not None else -1

    def update(self, update_columns, new_values, where_columns, where_values):
        self.updateGeneric(update_columns, new_values, where_columns, where_values)

    def delete(self, where_values, where_columns="CUSTOMER_ID"):
        self.deleteGeneric(where_columns, where_values)

    def get_row(self, select_columns="*", where_columns=None, where_values=None):
        return self.getRowGeneric(select_columns, where_columns, where_values)

    def get_table(self, select_columns="*", where_columns=None, where_values=None):
        return self.getTableGeneric(select_columns, where_columns, where_values)
