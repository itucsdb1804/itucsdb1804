from table_operations import book, category, book_category, person, customer, address, author, book_author, comment, customer_address, book_edition, transaction, product, transaction_product, control

class Database:
    def __init__(self):
        self.book = book.Book()
        self.category = category.Category()
        self.book_category = book_category.Book_Category()
        self.person = person.Person()
        self.customer = customer.Customer()
        self.address = address.Address()
        self.author = author.Author()
        self.book_author = book_author.Book_Author()
        self.comment = comment.Comment()
        self.customer_address = customer_address.CustomerAddress()
        self.book_edition = book_edition.BookEdition()
        self.transaction = transaction.Transaction()
        self.product = product.Product()
        self.transaction_product = transaction_product.TransactionProduct()
        self.control = control.Control()
