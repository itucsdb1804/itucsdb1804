from table_operations.baseClass import baseClass
from tables import Book_CategoryObj

class Book_Category(baseClass):
    def __init__(self):
        super().__init__("BOOK_CATEGORY", Book_CategoryObj)

    def add(self, book_id, category_id):
        query = self.insertIntoFlex("BOOK_ID", "CATEGORY_ID")
        fill = (book_id, category_id)
        self.execute(query, fill)
