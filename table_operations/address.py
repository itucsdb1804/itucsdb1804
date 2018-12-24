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
