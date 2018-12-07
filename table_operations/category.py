from table_operations.baseClass import baseClass
from tables import CategoryObj

class Category(baseClass):
    def __init__(self):
        super().__init__("CATEGORY", CategoryObj)

    def add(self, category_name):
        query = "INSERT INTO CATEGORY (CATEGORY_NAME) VALUES (%s)"
        fill = (category_name)
        self.execute(query, fill)

    def update(self, update_columns, new_values, where_columns, where_values):
        self.updateGeneric(update_columns, new_values, where_columns, where_values)

    def delete(self, where_values, where_columns="CATEGORY_ID"):
        self.deleteGeneric(where_columns, where_values)
    
    def get_row(self, select_columns="*", where_columns=None, where_values=None):
        return self.getRowGeneric(select_columns, where_columns, where_values)

    def get_table(self, select_columns="*", where_columns=None, where_values=None):
        return self.getTableGeneric(select_columns, where_columns, where_values)