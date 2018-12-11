import psycopg2 as dbapi2
import os
import sys

class baseClass:

    def __init__(self, table_name, constructor):
        self.tablename = table_name
        self.cons = constructor
        self.url = os.getenv("DATABASE_URL")
        if self.url is None:
            print("Usage: DATABASE_URL=url python database.py", file=sys.stderr)
            sys.exit(1)

    def convertToList(self, in_object):
        if type(in_object) is not list:
            if in_object is not None:
                return [in_object]
        
        return in_object


    def deleteGeneric(self, where_columns, where_values):
        '''
        @param where_columns (list), where_values (list)
        '''
        query = self.deleteFlex(where_columns)
        fill = (*where_values, )
        self.execute(query, fill)

    def updateGeneric(self, update_columns, new_values, where_columns, where_values):
        update_columns = self.convertToList(update_columns)
        new_values = self.convertToList(new_values)
        where_columns = self.convertToList(where_columns)
        where_values = self.convertToList(where_values)
        query = self.updateFlex(update_columns, where_columns)
        fill = (*new_values, *where_values)
        self.execute(query, fill)

    def getRowGeneric(self, select_columns, where_columns=None, where_values=None):
        select_columns = self.convertToList(select_columns)
        where_columns = self.convertToList(where_columns)
        where_values = self.convertToList(where_values)

        query = self.getRowFlex(select_columns, where_columns)
        fill = where_values if where_columns is not None else None

        result = self.execute(query, fill, True)

        if result is not None:
            result = result[0]
            if select_columns == ["*"]:
                result = self.cons(*result)
            else:
                result = result[0]
        return result

    def getTableGeneric(self, select_columns, where_columns=None, where_values=None):
        select_columns = self.convertToList(select_columns)
        where_columns = self.convertToList(where_columns)
        where_values = self.convertToList(where_values)

        results_list = []

        query = self.getTableFlex(select_columns, where_columns)
        fill = (*where_values, ) if where_columns is not None else None

        result = self.execute(query, fill, True)        
        if result is not None:
            for it in result:
                results_list.append(self.cons(*it))

        return results_list



    def whereFlex(self, where_columns):
        if where_columns is None: return ""
        col_count = len(where_columns)
        return (" WHERE {} = %s" + (col_count-1)*(" AND {} = %s")).format(*where_columns, )

    def insertIntoFlex(self, *insert_columns):
        col_count = len(insert_columns)
        valStr = ("%s, "*(col_count-1)) + "%s"
        columnStr = ("{}, "*(col_count-1)) + "{}"
        return ("INSERT INTO {tab} ("+columnStr+") VALUES ({fill})").format(tab=self.tablename, fill=valStr, *insert_columns, )

    def deleteFlex(self, *where_columns):
        return ("DELETE FROM {tab})"+self.whereFlex(where_columns)).format(tab=self.tablename, )

    def updateFlex(self, update_columns, where_columns):
        #columns shows the columns that will be updated
        valStr = ("{} = %s, "*(len(update_columns)-1) + "{} = %s ").format(*update_columns, )
        return ("UPDATE {tab} SET ".format(tab=self.tablename, ))+valStr+self.whereFlex(where_columns)

    def getRowFlex(self, select_columns="*", where_columns=None):
        selectStr = ("SELECT {}"+(", {}"*(len(select_columns)-1))).format(*select_columns)
        return selectStr+(" FROM {tab}").format(tab=self.tablename)+self.whereFlex(where_columns)

    def getTableFlex(self, select_columns="*", where_columns=None):
        selectStr = ("SELECT {}"+(", {}"*(len(select_columns)-1))).format(*select_columns)
        return selectStr+(" FROM {tab}".format(tab=self.tablename))+self.whereFlex(where_columns)



    def execute(self, query, fill=None, fetch_bool=False):
        result = []
        with dbapi2.connect(self.url) as connection:
            with connection.cursor() as curs:
                try:
                    print(curs.mogrify(query, fill))
                    curs.execute(query, fill)
                    if fetch_bool:
                        result = curs.fetchall()
                except dbapi2.Error as err:
                    print("Error: %s", err)
        
        return None if len(result) == 0 else result
