import os

import pyodbc


class DBConnString:
    def __init__(self, server, database, username, password, driver):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver


class SQLQuery:
    def __init__(self, table_name, **kwargs):
        self.table_name = table_name
        self.columns = kwargs

    def add_column(self, column_name, column_type):
        self.columns[column_name] = column_type

    def generate_query(self):
        query = f"CREATE TABLE {self.table_name} ("
        column_definitions = [f"id INT PRIMARY KEY"]  # first column
        for column_name, column_type in self.columns.items():
            column_definitions.append(f"{column_name} {column_type}")
        query += ", ".join(column_definitions)
        query += ");"
        return query


tquery_objectives = SQLQuery(table_name='objectives_completed',
                             main_objectives='INT',
                             optional_objectives='INT',
                             helldivers_extracted='INT',
                             outposts_destroyed_light='INT',
                             outposts_destroyed_medium='INT',
                             outposts_destoryed_heavy='INT',
                             mission_time_remaining='TIME'
                             ).generate_query()

tquery_samples = SQLQuery(table_name='samples_gained',
                          green_samples='INT',
                          orange_samples='INT',
                          violet_samples='INT'
                          ).generate_query()

tquery_currency = SQLQuery(table_name='currency_gained',
                           requisition='INT',
                           medals='INT',
                           xp='INT'
                           ).generate_query()

tquery_combat = SQLQuery(table_name='combat',
                         kills='INT',
                         accuracy="DECIMAL(5,2)",
                         shots_fired='INT',
                         deaths='INT',
                         stims_used='INT',
                         accidentals='INT',
                         samples_extracted='INT',
                         stratagems_used='INT',
                         melee_kills='INT',
                         times_reinforcing_='INT',
                         friendly_fire_damage='INT',
                         distance_travelled='INT',
                         ).generate_query()

# Create more connection string for other dbs or servers if You have them
Server1 = DBConnString(os.environ['AZURE_SERVER'], os.environ['AZURE_DATABASE'], os.environ['AZURE_SERVER_USERNAME'],
                       os.environ['AZURE_DB_PASSWORD'], '{ODBC Driver 18 for SQL Server}')


def connect(conn_string):
    try:
        conn = pyodbc.connect(f'DRIVER={conn_string.driver};SERVER={conn_string.server};'
                              f'DATABASE={conn_string.database};UID={conn_string.username};PWD={conn_string.password}')
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


def query_create_tables(server_name: str, table_queries: list) -> None:
    with connect(server_name).cursor() as cursor:
        for table_query in table_queries:
            cursor.execute(table_query)
        connect.commit()
        connect.close()
    print('Empty tables created')


# Print only row with specified ID
def query_read_row(table: str, row_number: int) -> None:
    with connect.cursor() as cursor:
        row = cursor.execute(f'SELECT * FROM {table} WHERE rowid = ?', (row_number,))
        print(row)
        connect.close()


# DONE
def query_read_table(table: str) -> None:
    with connect.cursor() as cursor:
        cursor.execute(f'SELECT * FROM {table}')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        connect.close()


#
def query_delete_table(table_name: str) -> None:
    sql_query = f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}"

    with connect.cursor() as cursor:
        cursor.execute(sql_query)
        connect.commit()
        connect().close()


# test this if it works
def query_update_cell(table_name: str, column_name: str, row_number: int, value: any) -> None:
    sql_query = f"UPDATE {table_name} SET {column_name} = {value} WHERE {row_number} = ?"

    with connect.cursor() as cursor:
        cursor.execute(sql_query)
        connect().commit()
        connect().close()


# write this
def query_delete_row(table_name: str, row_number: int) -> None:
    sql_query = f"DELETE FROM {table_name} WHERE rowid = {row_number}"

    with connect.cursor() as cursor:
        cursor.execute(sql_query)
        connect().commit()
        connect().close()


if __name__ == "__main__":
    query_tables = [tquery_objectives, tquery_samples, tquery_currency, tquery_samples]
    query_create_tables(Server1, query_tables)
    # query_delete_table('Employee')
