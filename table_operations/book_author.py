from table_operations.baseClass import baseClass
from tables import Book_AuthorObj

class Book_Author(baseClass):
    def __init__(self):
        super().__init__("BOOK_AUTHOR", Book_AuthorObj)

    def add(self, book_id, author_id):
        query = self.insertIntoFlex("BOOK_ID", "AUTHOR_ID")
        fill = (book_id, author_id)
        self.execute(query, fill)

    def delete(self, where_values, where_columns):
        self.deleteGeneric(where_columns, where_values)

    def get_row(self, select_columns="*", where_columns=None, where_values=None):
        return self.getRowGeneric(select_columns, where_columns, where_values)

    def get_table(self, select_columns="*", where_columns=None, where_values=None):
        return self.getTableGeneric(select_columns, where_columns, where_values)
