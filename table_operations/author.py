from table_operations.baseClass import baseClass
from tables import AuthorObj

class Author(baseClass):
    def __init__(self):
        super().__init__("AUTHOR", AuthorObj)

    def add(self, person_id, biography):
        query = self.insertIntoFlex("PERSON_ID", "BIOGRAPHY")
        fill = (person_id, biography)
        self.execute(query, fill)

    def update(self, values, condition, *columns):
        self.updateGeneric(values, condition, columns)

    def delete(self, value, condition="AUTHOR_ID"):
        self.deleteGeneric(value, condition)
    
    def get_row(self, condition, value, column="*"):
        return self.getRowGeneric(condition, value, column)

    def get_table(self, column="*"):
        return self.getTableGeneric(column)
