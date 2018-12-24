from table_operations.baseClass import baseClass
from tables import AddressObj

class Address(baseClass):
    def __init__(self):
        super().__init__("ADDRESS", AddressObj)

    def add(self, *values):
        '''
        @params address_name, country, city, district, neighborhood, avenue, street, addr_number, zipcode, explanation
        '''
        assert len(values) == 10
        query = self.insertIntoFlex("ADDRESS_NAME", "COUNTRY", "CITY", "DISTRICT", "NEIGHBORHOOD", "AVENUE", "STREET", "ADDR_NUMBER", "ZIPCODE", "EXPLANATION")
        fill = (*values, )
        self.execute(query, fill)


    def update(self, update_columns, new_values, where_columns, where_values):
        self.updateGeneric(update_columns, new_values, where_columns, where_values)

    def delete(self, where_values, where_columns="ADDRESS_ID"):
        self.deleteGeneric(where_columns, where_values)

    def get_row(self, select_columns="*", where_columns=None, where_values=None):
        return self.getRowGeneric(select_columns, where_columns, where_values)

    def get_table(self, select_columns="*", where_columns=None, where_values=None):
        return self.getTableGeneric(select_columns, where_columns, where_values)
