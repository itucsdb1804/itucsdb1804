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
