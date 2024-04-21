from typing import Literal
import sqlite3
import csv
import pathlib
import psycopg2


#TODO
# Update Table function
# External event listener
# SQL Functions and Triggers
# Postgres TYPEDEF interface
# Expose more DBMS capabilities

POSTGRES_TYPES = {"integer": "integer", "smallint": "smallint", "bigint": "bigint", 
                  "float4": "real", "float8": "double precision", "decimal": "decimal", "numeric": "numeric", 
                  "string": "text", 
                  "geometry": "text", 
                  "epoch_seconds": "integer", "epoch_milliseconds": "real", "timestamp_tz": "timestamp with time zone", "timestamp": "timestamp",
                  "date": "date", "time_tz": "time with time zone", "time": "time", "interval": "interval",
                  "id": "uuid", "json": "json", "jsonb": "jsonb"}

SQLITE_TYPES = {"integer": "INTEGER", "smallint": "INTEGER", "bigint": "INTEGER", 
                "float4": "REAL", "float8": "REAL", "decimal": "REAL", "numeric": "REAL", 
                "string": "TEXT", 
                "geometry": "TEXT", 
                "epoch_seconds": "INTEGER", "epoch_milliseconds": "REAL", "timestamp_tz": "TEXT", "timestamp": "TEXT", 
                "date": "TEXT", "time_tz": "TEXT", "time": "TEXT", "interval": "TEXT",
                "id": "id", "json": "TEXT", "jsonb": "TEXT"}


POSGRES_BINDING = "%s"
SQLITE_BINDING = "?"

ALTER_COL_OP = Literal["DROP", "ADD", "ALTER", "RENAME COLUMN", "RENAME TABLE"]
DB_TYPE_LIST = Literal["integer", "smallint", "bigint", "float4", "float8", "decimal", "numeric", "string", "geometry", "timestamp_tz", "timestamp",
                       "date", "time_tz", "time", "id", "json", "jsonb"]

class DatabaseInterface:
    def __init__(self):
        self.__db_conn = None
        self.__type_map = None
        self.__binding_char = None
    
    @property
    def db_conn(self):
        return self.__db_conn
    
    def set_sqlite_connection(self, db_path:str):
        self.__db_conn = sqlite3.Connection(db_path)
        self.__type_map = SQLITE_TYPES
        self.__binding_char = SQLITE_BINDING
    
    def set_postgres_connection(self, db_name:str, username:str, password:str, host="localhost", port=5432, postgis=False):
        self.__db_conn = psycopg2.connect(database=db_name, user=username, password=password, host=host, port=port)
        self.__type_map = POSTGRES_TYPES
        self.__binding_char = POSGRES_BINDING
        if postgis:
            self.__type_map["geometry"] = "geometry"
        else:
            self.__type_map["geometry"] = "text"
        

    def list_tables(self):
        """Returns a list of tables located within the connected database."""
        if type(self.db_conn) == sqlite3.Connection:
            cur = self.db_conn.cursor()
            res = cur.execute("SELECT name FROM sqlite_master").fetchall()
            return [table[0] for table in res]
        elif type(self.db_conn) == psycopg2.extensions.connection:
            cur = self.db_conn.cursor()
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            return [table[0] for table in cur.fetchall()]

    def __ambiguous_type(self, records, col_name):
        for row in records:
            if row[col_name]:
                return self.__infer_type(row[col_name])
        return self.__type_map["string"]

    def __infer_type(self, val:str):
        if type(val) == int or type(val) == float:
            if type(val) == int:
                dtype = self.__type_map["integer"]
            elif type(val) == float:
                dtype = self.__type_map["float8"]
        else:
            val:str
            split = val.split(".")
            if len(split) == 2:
                if split[0].isnumeric() and split[1].isnumeric():
                    if len(split[1]) > 8:
                        dtype = self.__type_map["float8"]
                    else:
                        dtype = self.__type_map["float4"]
                else:
                    dtype = self.__type_map["string"]
            elif val.isnumeric():
                if val == "0":
                    dtype = self.__type_map["numeric"]
                else:
                    dtype = self.__type_map["integer"]
            else:
                dtype = self.__type_map["string"]
            
        return dtype
    
    def __infer_schema(self, records:list[dict], schema_override:list[dict]=[{"col_name": "", "data_type": ""}]):
        schema = []
        top_row:dict = records[0]
        col_overrides = tuple(col['col_name'] for col in schema_override)
        
        position = 1
        for col_name, value in top_row.items():
            if col_name in col_overrides:
                i = col_overrides.index(col_name)
                schema.append({"position": position, "col_name": col_name, "data_type": self.__type_map[schema_override[i]["data_type"]]})
            else:
                if value:
                    data_type = self.__infer_type(value)
                else:
                    data_type = self.__ambiguous_type(records, col_name)
                schema.append({"position": position, "col_name": col_name, "data_type": data_type})
            position += 1
    
        return schema
    
    def __create_table_statement(self, table_name:str, table_schema:list[dict]):
        statement = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for col in table_schema:
            statement += f"{col['col_name']} {col['data_type']}, "
        statement = statement[:-2] + f")"
        return statement
    
    def __select_table_statement(self, table_name:str, columns:str="*", where_clause:str=""):
        statement = f"SELECT {columns} FROM {table_name}"
        if where_clause:
            statement += f" {where_clause}"
        return statement
    
    def __insert_into_table_statement(self, table_name:str, table_schema:list[dict]):
        statement = f"INSERT INTO {table_name} ("
        bindings = ""
        for col in table_schema:
            statement += f"{col['col_name']}, "
            bindings += f"{self.__binding_char}, "
        statement = statement[:-2] + f") VALUES (" + bindings[:-2] + ")"
        return statement
    
    def __update_table_statement(self):
        pass

    def get_schema(self, table_name:str):
        """Returns a list of dictionaries representing information about a table's schema.\n{"position": 1, "col_name": col1, "data_type": integer}"""
        if type(self.db_conn) == sqlite3.Connection:
            cur = self.db_conn.cursor()
            res = cur.execute(f"PRAGMA table_info({table_name})").fetchall()
            return [{"position": (row[0] + 1), "col_name": row[1], "data_type": row[2]} for row in res]
        elif type(self.db_conn) == psycopg2.extensions.connection:
            cur = self.db_conn.cursor()
            cur.execute(f"SELECT ordinal_position, column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'")
            schema = [{"position": row[0], "col_name": row[1], "data_type": row[2]} for row in cur.fetchall()]
            schema = sorted(schema, key=lambda x : x['position'])
            return schema
    
    def get_table(self, table_name:str, columns:str="*", where_clause:str=""):
        """
        Queries the database for a table, returns standard list of tuples representing rows of the table.\n
        table_name 
            - Name of the table\n
        columns (Optional)
            - column name filter separated by commas (col1, col2, col3)
            - Defaults to *\n
        where_clause (Optional)
            - where option for more refine queries
            - must include the "WHERE"
            - Defaults to "" (Empty)
        """
        select_statement = self.__select_table_statement(table_name, columns, where_clause)
        
        if type(self.db_conn) == sqlite3.Connection:
            cur = self.db_conn.cursor()
            res = cur.execute(select_statement).fetchall()
            return res
        elif type(self.db_conn) == psycopg2.extensions.connection:
            cur = self.db_conn.cursor()
            cur.execute(select_statement)
            return cur.fetchall()

    def table_from_records(self, table_name:str, table_records:list[dict], schema_override:list[dict]=[{"col_name": "", "data_type": ""}]):
        """
        Creates a new database table from a list of records.\n
        table_name 
            - Name of the table\n
        table_records
            - A list of dictionaries representing table records
            - [{"col1": "val1", "col2": "val2"}, {"col1": "val1", "col2": "val2"}]\n
        schema_override (Optional)
            - An option to explicitly set a column's datatype
            - Format: [{"col_name": <COLUMN NAME>, "data_type": <DESIRED DATA TYPE>}]
            - DESIRED DATA TYPE: integer, float4, float8, string, timestamp, datetime, geometry
        """
        table_schema = self.__infer_schema(table_records, schema_override)
        create_statement = self.__create_table_statement(table_name, table_schema)
        insert_statement = self.__insert_into_table_statement(table_name, table_schema)
        table_records_sql = [tuple(val for val in row.values()) for row in table_records]

        cur = self.db_conn.cursor()
        cur.execute(create_statement)
        cur.executemany(insert_statement, table_records_sql)
        self.db_conn.commit()
    
    def append_records(self, table_name:str, table_records:list[dict]):
        table_schema = self.get_schema(table_name)
        insert_statement = self.__insert_into_table_statement(table_name, table_schema)
        table_records_sql = [tuple(val for val in row.values()) for row in table_records]

        cur = self.db_conn.cursor()
        cur.executemany(insert_statement, table_records_sql)
        self.db_conn.commit()

    def append_csv(self, table_name:str, csv_path:str):
        csv_path:pathlib.Path = pathlib.Path(csv_path)
        with open(csv_path, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            records = [row for row in reader]
        self.append_records(table_name, records)

    def csv_to_records(self, csv_path:str):
        csv_path:pathlib.Path = pathlib.Path(csv_path)
        with open(csv_path, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            records = [row for row in reader]
        
        for row in records:
            for key, val in row.items():
                if val == '':
                    row[key] = None
    
        return records

    def csv_to_table(self, csv_path:str, schema_override:list[dict]=[{"col_name": "", "data_type": ""}]):
        """
        Reads a csv file and migrates into a new database table.\n
        When evaluating the schema, only the top row is checked for data types.
        """
        csv_name = pathlib.Path(csv_path).stem
        records = self.csv_to_records(csv_path)
        if csv_name in self.get_tables():
            print(f"{csv_name} is already a table in the database. You can alternatively use append_csv() if this is intended")
            return
        self.table_from_records(csv_name, records, schema_override)

    def table_to_records(self, table_name:str, columns:str="*", where_clause:str=""):
        """
        Queries the database for a table, returns a list of dictionaries representing table rows.\n
        [{"col1": "val1", "col2": "val2"}, {"col1": "val1", "col2": "val2"}]\n
        table_name 
            - Name of the table\n
        columns (Optional)
            - column name filter separated by commas (col1, col2, col3)
            - Defaults to *\n
        where_clause (Optional)
            - where option for more refine queries
            - must include the "WHERE"
            - Defaults to "" (Empty)
        """
        schema = self.get_schema(table_name)
        table_data = self.get_table(table_name, columns, where_clause)

        if columns != "*":
            col_names = columns.split(", ")
            schema = [col for col in schema if col['col_name'] in col_names]

        records = []
        for row in table_data:
            record_row = {}
            for col in range(len(schema)):
                record_row[schema[col]['col_name']] = row[col]
            records.append(record_row)

        return records
    
    def table_to_csv(self, table_name:str, save_path:str=".", columns:str="*", where_clause:str=""):
        """
        Queries the database for a table, then writes its contents into csv.\n
        table_name 
            - Name of the table\n
        save_path
            - Save location of the csv
            - Do not include a filename, table name is used.\n
        columns (Optional)
            - column name filter separated by commas (col1, col2, col3)
            - Defaults to *\n
        where_clause (Optional)
            - where option for more refine queries
            - must include the "WHERE"
            - Defaults to "" (Empty)
        """
        table_records = self.table_to_records(table_name, columns, where_clause)
        headers:dict = table_records[0]
        headers = headers.keys()

        with open(f"{save_path}\\{table_name}.csv", 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(table_records)
            
    def drop_table(self, table_name):
        cur = self.db_conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.db_conn.commit()

    def alter_table(self, table_name, col_name, alter_col_op:ALTER_COL_OP, data_type:DB_TYPE_LIST="", new_col_name:str="", new_table_name:str=""):
        cur = self.db_conn.cursor()
        if alter_col_op == "ADD":
            op = f"ADD {col_name} {self.__type_map[data_type]}"
        elif alter_col_op =="DROP":
            op = f"DROP COLUMN {col_name}"
        elif alter_col_op == "RENAME COLUMN" and new_col_name:
            op = f"RENAME COLUMN {col_name} TO {new_col_name}"
        elif alter_col_op == "RENAME TABLE" and new_table_name:
            op = f"RENAME TO {new_table_name}"
        elif alter_col_op == "ALTER":
            if type(self.db_conn) == sqlite3.Connection:
                raise Exception("Sqlite3 is not capable of modifying column data type")
            op = f"ALTER COLUMN {col_name} {self.__type_map[data_type]}"
        
        sql_statement = f"ALTER TABLE {table_name} {op}"
        cur.execute(sql_statement)
        self.db_conn.commit()





def table_migrate(source_db:DatabaseInterface, dest_db:DatabaseInterface, table_name, dest_table_name=None, schema_override:list[dict]=[{"col_name": "", "data_type": ""}]):
    source_table_records = source_db.table_to_records(table_name)
    if dest_table_name:
        dest_db.table_from_records(dest_table_name, source_table_records, schema_override)
    else:
        dest_db.table_from_records(table_name, source_table_records, schema_override)