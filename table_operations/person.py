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
        query = self.insertIntoFlex("PERSON_NAME", "SURNAME", "GENDER", "DATE_OF_BIRTH", "NATIONALITY") + " RETURNING PERSON_ID"
        fill = (*values, )
        last_person_id = (self.execute(query, fill, True))[0][0]
        return last_person_id if last_person_id is not None else -1


    def update(self, update_columns, new_values, where_columns, where_values):
        self.updateGeneric(update_columns, new_values, where_columns, where_values)

    def delete(self, where_values, where_columns="PERSON_ID"):
        self.deleteGeneric(where_columns, where_values)
    
    def get_row(self, select_columns="*", where_columns=None, where_values=None):
        return self.getRowGeneric(select_columns, where_columns, where_values)

    def get_table(self, select_columns="*", where_columns=None, where_values=None):
        return self.getTableGeneric(select_columns, where_columns, where_values)