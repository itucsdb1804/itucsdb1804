from table_operations.baseClass import baseClass
from tables import AuthorObj

class Author(baseClass):
    def __init__(self):
        super().__init__("AUTHOR", AuthorObj)

    def add(self, person_id, biography):
        query = self.insertIntoFlex("PERSON_ID", "BIOGRAPHY")
        fill = (person_id, biography)
        self.execute(query, fill)
