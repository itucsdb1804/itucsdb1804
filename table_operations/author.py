from table_operations.baseClass import baseClass
from tables import AuthorObj

class Author(baseClass):
    def __init__(self):
        super().__init__("AUTHOR", AuthorObj)

    def add(self, person_id, biography):
        query = self.insertIntoFlex("PERSON_ID", "BIOGRAPHY")
        fill = (person_id, biography)
        self.execute(query, fill)

    def update(self, update_columns, new_values, where_columns, where_values):
        self.updateGeneric(update_columns, new_values, where_columns, where_values)

    def delete(self, where_values, where_columns="AUTHOR_ID"):
        self.deleteGeneric(where_columns, where_values)

    def get_row(self, select_columns="*", where_columns=None, where_values=None):
        return self.getRowGeneric(select_columns, where_columns, where_values)

    def get_table(self, select_columns="*", where_columns=None, where_values=None):
        return self.getTableGeneric(select_columns, where_columns, where_values)
