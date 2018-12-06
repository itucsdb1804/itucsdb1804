from table_operations.baseClass import baseClass
from tables import CategoryObj

class Category(baseClass):
    def __init__(self):
        super().__init__("CATEGORY", CategoryObj)

    def add(self, category_name):
        query = "INSERT INTO CATEGORY (CATEGORY_NAME) VALUES (%s)"
        fill = (category_name)
        self.execute(query, fill)

    def update(self, values, condition, *columns):
        self.updateGeneric(values, condition, columns)

    def delete(self, value, condition="CATEGORY_ID"):
        self.deleteGeneric(value, condition)
    
    def get_row(self, condition, value, column="*"):
        return self.getRowGeneric(condition, value, column)

    def get_table(self, column="*"):
        return self.getTableGeneric(column)