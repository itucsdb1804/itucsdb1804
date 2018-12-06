from table_operations.baseClass import baseClass
from tables import PersonObj

class Person(baseClass):
    def __init__(self):
        super().__init__("PERSON", PersonObj)

    def add(self, *values):
        '''
        @param person_name, person_surname, gender, date_of_birth, nationality
        '''
        assert len(values) == 5
        query = self.insertIntoFlex("PERSON_NAME", "SURNAME", "GENDER", "DATE_OF_BIRTH", "NATIONALITY") + "RETURNING PERSON_ID"
        fill = (*values, )
        last_id = self.execute(query, fill)[0]
        return last_id if last_id != None else -1


    def update(self, values, condition, *columns):
        self.updateGeneric(values, condition, columns)

    def delete(self, value, condition="PERSON_ID"):
        self.deleteGeneric(value, condition)
    
    def get_row(self, condition, value, column="*"):
        return self.getRowGeneric(condition, value, column)

    def get_table(self, column="*"):
        return self.getTableGeneric(column)