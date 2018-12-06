from table_operations.baseClass import baseClass
from tables import Book_CategoryObj

class Book_Category(baseClass):
    def __init__(self):
        super().__init__("BOOK_CATEGORY", Book_CategoryObj)

    def add(self, book_id, category_id):
        query = self.insertIntoFlex("BOOK_ID", "CATEGORY_ID")
        fill = (book_id, category_id)
        self.execute(query, fill)

    def update(self, value, condition, column):
        self.updateGeneric(value, condition, column)

    def delete(self, value, condition):
        self.deleteGeneric(value, condition)
    
    def get_row(self, condition, value, column="*"):
        return self.getRowGeneric(condition, value, column)

    def get_table(self, column="*"):
        return self.getTableGeneric(column)