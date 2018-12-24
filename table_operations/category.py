from table_operations.baseClass import baseClass
from tables import CategoryObj

class Category(baseClass):
    def __init__(self):
        super().__init__("CATEGORY", CategoryObj)

    def add(self, category_name):
        query = "INSERT INTO CATEGORY (CATEGORY_NAME) VALUES (%s)"
        fill = (category_name)
        self.execute(query, fill)
