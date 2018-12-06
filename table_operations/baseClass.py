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


    def deleteGeneric(self, value, condition):
        query = self.deleteFlex(condition)
        fill = (value, )
        self.execute(query, fill)

    def updateGeneric(self, values, condition, *columns):
        query = self.updateFlex(condition, len(values), *columns)
        fill = (*values, )
        self.execute(query, fill)

    def getRowGeneric(self, condition, value, column):
        query = self.getRowFlex(condition, column)
        fill = (value, )

        result = self.execute(query, fill)
        if result is not None:
            result = result[0]
            if column == "*":
                result = self.cons(*result, )
            else:
                result = result[0]
        return result

    def getTableGeneric(self, column):
        results_list = []

        query = self.getTableFlex(column)
        result = self.execute(query)
        
        if result is not None:
            for it in result:
                results_list.append(self.cons(*it))

        return results_list


    def insertIntoFlex(self, *columns):
        col_count = len(columns)
        valStr = ("%s, "*(col_count-1)) + "%s"
        columnStr = ("{}, "*(col_count-1)) + "{}"
        return ("INSERT INTO {tab} ("+columnStr+") VALUES ({fill})").format(tab=self.tablename, fill=valStr, *columns, )

    def deleteFlex(self, condition):
        return "DELETE FROM {tab} WHERE {cond} = %s".format(tab=self.tablename, cond=condition)

    def updateFlex(self, condition, *columns):
        #columns shows the columns that will be updated
        valStr = ("{} = %s, "*(len(columns)-1)) + "{} = %s "
        return ("UPDATE {tab} SET "+valStr+"WHERE {cond} = %s").format(tab=self.tablename, cond=condition, *columns, )

    def getRowFlex(self, condition, column="*"):
        return "SELECT {col} FROM {tab} WHERE {cond} = %s".format(col=column, tab=self.tablename, cond=condition)

    def getTableFlex(self, column="*"):
        return "SELECT {col} FROM {tab}".format(col=column, tab=self.tablename)


    def execute(self, query, fill=None):
        result = []
        with dbapi2.connect(self.url) as connection:
            with connection.cursor() as curs:
                try:
                    print(curs.mogrify(query, fill))
                    curs.execute(query, fill)
                    result = curs.fetchall()
                except dbapi2.Error as err:
                    print("Error: %s", err)
        
        return None if len(result) == 0 else result
