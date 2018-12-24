from table_operations.baseClass import baseClass
from tables import Book_CategoryObj

class Book_Category(baseClass):
    def __init__(self):
        super().__init__("BOOK_CATEGORY", Book_CategoryObj)

    def add(self, book_id, category_id):
        query = self.insertIntoFlex("BOOK_ID", "CATEGORY_ID")
        fill = (book_id, category_id)
        self.execute(query, fill)

    def update(self, update_columns, new_values, where_columns, where_values):
        self.updateGeneric(update_columns, new_values, where_columns, where_values)

    def delete(self, where_values, where_columns):
        self.deleteGeneric(where_columns, where_values)

    def get_row(self, select_columns="*", where_columns=None, where_values=None):
        return self.getRowGeneric(select_columns, where_columns, where_values)

    def get_table(self, select_columns="*", where_columns=None, where_values=None):
        return self.getTableGeneric(select_columns, where_columns, where_values)
