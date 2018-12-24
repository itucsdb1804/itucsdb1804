from table_operations.baseClass import baseClass
from tables import Book_AuthorObj

class Book_Author(baseClass):
    def __init__(self):
        super().__init__("BOOK_AUTHOR", Book_AuthorObj)

    def add(self, book_id, author_id):
        query = self.insertIntoFlex("BOOK_ID", "AUTHOR_ID")
        fill = (book_id, author_id)
        self.execute(query, fill)
