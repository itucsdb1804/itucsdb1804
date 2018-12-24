import os
import sys
import psycopg2 as dbapi2

url = os.getenv("DATABASE_URL")
if url is None:
    print("Usage: DATABASE_URL=url python database.py", file=sys.stderr)
    sys.exit(1)

class baseClass:

    def __init__(self, table_name, constructor):
        self.tablename = table_name
        self.cons = constructor


    def deleteGeneric(self, where_columns, where_values):
        where_columns = convertToList(where_columns)
        where_values = convertToList(where_values)
        query = deleteFlex(self.tablename, *where_columns)
        fill = (*where_values, )
        self.execute(query, fill)


    def update(self, update_columns, new_values, where_columns, where_values):
        update_columns = convertToList(update_columns)
        new_values = convertToList(new_values)
        where_columns = convertToList(where_columns)
        where_values = convertToList(where_values)
        query = updateFlex(self.tablename, update_columns, where_columns)
        fill = (*new_values, *where_values)
        self.execute(query, fill)


    def getRowGeneric(self, select_columns, where_columns=None, where_values=None):
        select_columns = convertToList(select_columns)
        where_columns = convertToList(where_columns)
        where_values = convertToList(where_values)

        query = getFlex(self.tablename, select_columns, where_columns)
        fill = where_values if where_columns is not None else None

        result = self.execute(query, fill, True)

        if result is not None:
            result = self.cons(*result[0]) if select_columns == ["*"] else (result[0])[0]
        return result


    def getTableGeneric(self, select_columns, where_columns=None, where_values=None):
        select_columns = convertToList(select_columns)
        where_columns = convertToList(where_columns)
        where_values = convertToList(where_values)

        results_list = []

        query = getFlex(self.tablename, select_columns, where_columns)
        fill = (*where_values, ) if where_columns is not None else None

        result = self.execute(query, fill, True)
        if result is not None:
            for elem_it in result:
                if select_columns == ["*"]:
                    results_list.append(self.cons(*elem_it))
                else:
                    results_list.append(elem_it[0])
        return results_list


    def insertIntoFlex(self, *insert_columns):
        col_count = len(insert_columns)
        val_str = ("%s, "*(col_count-1)) + "%s"
        column_str = ("{}, "*(col_count-1)) + "{}"
        return ("INSERT INTO {tab} ("+column_str+") VALUES ({fill})").format(tab=self.tablename, fill=val_str, *insert_columns, )


    def execute(self, query, fill=None, fetch_bool=False):
        result = []
        with dbapi2.connect(url) as connection:
            with connection.cursor() as curs:
                try:
                    print(curs.mogrify(query, fill))
                    curs.execute(query, fill)
                    if fetch_bool:
                        result = curs.fetchall()
                except dbapi2.Error as err:
                    print("Error: ", err)

        return None if not result else result




def deleteFlex(tablename, *where_columns):
    return ("DELETE FROM {tab}".format(tab=tablename, ))+whereFlex(where_columns)


def updateFlex(tablename, update_columns, where_columns):
    val_str = ("{} = %s, "*(len(update_columns)-1) + "{} = %s ").format(*update_columns, )
    return ("UPDATE {tab} SET ".format(tab=tablename, ))+val_str+whereFlex(where_columns)


def getFlex(tablename, select_columns="*", where_columns=None):
    select_str = ("SELECT {}"+(", {}"*(len(select_columns)-1))).format(*select_columns)
    return select_str+(" FROM {tab}").format(tab=tablename)+whereFlex(where_columns)


def whereFlex(where_columns):
    if where_columns is None:
        return ""
    col_count = len(where_columns)
    return (" WHERE {} = %s" + (col_count-1)*(" AND {} = %s")).format(*where_columns, )


def convertToList(in_object):
    if not isinstance(in_object, list):
        if in_object is not None:
            return [in_object]
    return in_object
