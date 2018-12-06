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
        query = self.insertIntoFlex("PERSON_ID", "USERNAME", "EMAIL", "PASS_HASH", "PHONE", "IS_ACTIVE")
        fill = (*values, )
        self.execute(query, fill)

    def update(self, values, condition, *columns):
        self.updateGeneric(values, condition, columns)

    def delete(self, value, condition="CUSTOMER_ID"):
        self.deleteGeneric(value, condition)
    
    def get_row(self, condition, value, column="*"):
        return self.getRowGeneric(condition, value, column)

    def get_table(self, column="*"):
        return self.getTableGeneric(column)