from .database import Database
import sqlite3
import csv
from typing import Literal
import pathlib

from .schema_objects import SQLColumn, SQLSchema

SQLITE_TYPES = Literal["text", "real", "integer", "numeric"]

SQLITE_TYPE_MAP = {"integer": "integer", "smallint": "integer", "bigint": "integer", 
                   "real": "real", "double precision": "real", "decimal": "real", "numeric": "numeric",  
                   "smallserial": "integer", "serial": "integer", "bigserial": "integer", "geometry": "text", 
                   "text": "text", "timestamp": "text", "timestamp with time zone": "text",
                   "date": "text", "time with timezone": "text", "time": "text", "boolean": "text",
                   "uuid": "text", "interval": "text",  "json": "text", "jsonb": "text"}

class SQLite(Database):
    def __init__(self, sqlite_path:str, foreign_keys_on=False, type_map=SQLITE_TYPE_MAP):
        self.__db_conn = sqlite3.Connection(sqlite_path)
        self.__binding_char = "?"
        self.__type_map = type_map
        if foreign_keys_on:
            cur = self.db_conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            resp = cur.execute("PRAGMA foreign_keys")
            print(f"Foreign Keys for {sqlite_path}:", bool(resp.fetchall()[0][0]))
    
    @property
    def db_conn(self):
        return self.__db_conn
    
    def table_from_records(self, table_name:str, table_records:list[dict], col_overrides:list[SQLColumn]=[], schema_override:SQLSchema=None) -> None:
        schema:SQLSchema = schema_override
        if not schema_override:
            schema = self.evaluate_schema(table_records, col_overrides)

        create_statement = self.create_table_statement(table_name, schema)
        insert_statement = self.insert_into_table_statement(table_name, schema)
        table_records_sql = [tuple(val for val in row.values()) for row in table_records]

        cur = self.db_conn.cursor()
        cur.execute(create_statement)
        cur.executemany(insert_statement, table_records_sql)
        self.db_conn.commit()

    def table_append_records(self, table_name:str, table_records:list[dict]) -> None:
        schema = self.get_schema(table_name)
        schema.filter_columns(list(table_records[0].keys()))
        
        insert_statement = self.insert_into_table_statement(table_name, schema)
        table_records_sql = [tuple(val for val in row.values()) for row in table_records]

        cur = self.db_conn.cursor()
        cur.executemany(insert_statement, table_records_sql)
        self.db_conn.commit()

    def update_with_unique_records(self, table_name:str, records:list[dict], unique_key_col:str) -> None:
        cur = self.db_conn.cursor()
        for row in records:
            update_statement = self.create_update_statement(table_name, row, f"WHERE {unique_key_col}='{row[unique_key_col]}'")
            cur.execute(update_statement)
        self.db_conn.commit()

    def delete_rows(self, table_name:str, where_clause:str) -> None:
        cur = self.db_conn.cursor()
        delete_statement = self.create_delete_statement(table_name, where_clause)
        print(delete_statement)
        cur.execute(delete_statement)
        self.db_conn.commit()

    def append_csv_to_table(self, table_name:str, csv_path:str) -> None:
        csv_path:pathlib.Path = pathlib.Path(csv_path)
        with open(csv_path, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            records = [row for row in reader]
        self.table_append_records(table_name, records)

    def records_to_csv(self, records:list[dict], csv_name:str, csv_path:str) -> None:
        headers = records[0].keys()
        with open(f"{csv_path}\\{csv_name}.csv", "w", newline='') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(records)

    def create_blank_table(self, table_name:str, schema:SQLSchema) -> None:
        sql = self.create_table_statement(table_name, schema)
        print(sql)
        cur = self.db_conn.cursor()
        cur.execute(sql)
        
    def csv_to_records(self, csv_path:str) -> list[dict]:
        csv_path:pathlib.Path = pathlib.Path(csv_path)
        with open(csv_path, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            records = [row for row in reader]
        
        for row in records:
            for key, val in row.items():
                if val == '':
                    row[key] = None
    
        return records
    
    def csv_to_table(self, csv_path:str, col_overrides:list[SQLColumn]=[], schema_override:SQLSchema=None) -> None:
        csv_name = pathlib.Path(csv_path).stem
        records = self.csv_to_records(csv_path)
        if csv_name in self.list_tables():
            print(f"{csv_name} is already a table in the database. You can alternatively use append_csv() if this is intended")
            return
        self.table_from_records(csv_name, records, col_overrides, schema_override)

    def table_to_records(self, table_name:str, columns:str="*", where_clause:str="") -> list[dict]:
        schema:SQLSchema = self.get_schema(table_name)
        table_data = self.get_table(table_name, columns, where_clause)

        if columns != "*":
            schema.filter_columns(columns.split(", "))
            
        records = []
        for row in table_data:
            record_row = {}
            for col_name, sql_col in schema.schema_map.items():
                record_row[col_name] = row[sql_col.position - 1]
            records.append(record_row)

        return records

    def table_to_csv(self, table_name:str, save_path:str=".", columns:str="*", where_clause:str="") -> None:
        table_records = self.table_to_records(table_name, columns, where_clause)
        headers:dict = table_records[0]
        headers = headers.keys()

        with open(f"{save_path}\\{table_name}.csv", 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(table_records)
            
    def drop_table(self, table_name) -> None:
        cur = self.db_conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.db_conn.commit()

    def delete_all_records(self, table_name:str) -> None:
        cur = self.db_conn.cursor()
        cur.execute(f"DELETE FROM {table_name}")
        self.db_conn.commit()

    def add_column(self, table_name:str, col_name:str, data_type:SQLITE_TYPES):
        cur = self.db_conn.cursor()
        sql_statement = f"ALTER TABLE {table_name} ADD {col_name} {self.__type_map[data_type]}"
        cur.execute(sql_statement)
        self.db_conn.commit()
    
    def drop_column(self, table_name:str, col_name:str):
        cur = self.db_conn.cursor()
        sql_statement = f"ALTER TABLE {table_name} DROP COLUMN {col_name}"
        cur.execute(sql_statement)
        self.db_conn.commit()
    
    def rename_column(self, table_name:str, col_name:str, new_col_name:str):
        cur = self.db_conn.cursor()
        sql_statement = f"ALTER TABLE {table_name} RENAME COLUMN {col_name} TO {new_col_name}"
        cur.execute(sql_statement)
        self.db_conn.commit()

    def rename_table(self, table_name:str, new_table_name:str):
        cur = self.db_conn.cursor()
        sql_statement = f"ALTER TABLE {table_name} RENAME TO {new_table_name}"
        cur.execute(sql_statement)
        self.db_conn.commit()

    def list_tables(self) -> list[str]:
        cur = self.db_conn.cursor()
        res = cur.execute("SELECT name FROM sqlite_master").fetchall()
        return [table[0] for table in res]

    def get_schema(self, table_name:str) -> SQLSchema:
        cur = self.db_conn.cursor()
        res = cur.execute(f"PRAGMA table_info({table_name})").fetchall()
        if not res:
            print(f"No data returned from table '{table_name}'")
            return
        return SQLSchema([SQLColumn(name=row[1], data_type=row[2], position=(row[0] + 1), nullable=bool(row[3]), is_primary_key=bool(row[5])) for row in res])
    
    def get_table(self, table_name:str, columns:str="*", where_clause:str="") -> list[tuple]:
        select_statement = self.select_table_statement(table_name, columns, where_clause)
        cur = self.db_conn.cursor()
        res = cur.execute(select_statement).fetchall()
        return res
    
    def infer_type(self, val:str) -> str:
        if type(val) == int or type(val) == float:
            if type(val) == int:
                return "integer"
            elif type(val) == float:
                return "real"
        elif type(val) == bool:
            return "text"
        else:
            val:str
            split = val.split(".")
            if len(split) == 2:
                if split[0].isnumeric() and split[1].isnumeric():
                    return "real"
                else:
                    return "text"
            elif val.isnumeric():
                if val == "0":
                    return "numeric"
                else:
                    return "integer"
            else:
                return "text"
            
    def evaluate_schema(self, records:list[dict], col_overrides:list[SQLColumn]=[]) -> SQLSchema:

        def find_non_null_record(records:list[dict], col_name:str):
            for row in records:
                if row[col_name]:
                    return row[col_name]
            return "empty_col_default_to_string"

        schema = []
        top_row:dict = records[0]
        overide_col_list = tuple(col.name for col in col_overrides)

        pos = 1
        for col_name, col_val in top_row.items():
            if col_name in overide_col_list:
                col:SQLColumn = col_overrides[overide_col_list.index(col_name)]
                schema.append(SQLColumn(name=col.name, data_type=self.__type_map[col.data_type], position=pos, 
                                        not_null=col.nullable, is_primary_key=col.is_primary_key, foreign_key=col.foreign_key))
            else:
                if col_val:
                    d_type = self.infer_type(col_val)
                else:
                    d_type = self.infer_type(find_non_null_record(records, col_name))
                
                schema.append(SQLColumn(name=col_name, data_type=d_type, position=pos))
            pos += 1
        return SQLSchema(schema)
    
    def select_table_statement(self, table_name:str, columns:str="*", where_clause:str="") -> str:
        statement = f"SELECT {columns} FROM {table_name}"
        if where_clause:
            statement += f" {where_clause}"
        return statement
    
    def create_update_statement(self, table_name:str, record_row:dict, where_clause:str) -> str:
        statement = f"UPDATE {table_name} SET "
        for col_name, value in record_row.items():
            statement += f"{col_name}='{value}', "
        statement = statement[:-2] + " " + where_clause
        return statement

    def create_delete_statement(self, table_name:str, where_clause:str="") -> str:
        statement = f"DELETE FROM {table_name}"
        if where_clause:
            statement += f" {where_clause}"
        return statement

    def insert_into_table_statement(self, table_name:str, schema:SQLSchema) -> str:
        statement = f"INSERT INTO {table_name} ("
        bindings = ""
        for col_name, sql_col in schema.schema_map.items():
            statement += f"{col_name}, "
            bindings += f"{self.__binding_char}, "
        statement = statement[:-2] + f") VALUES (" + bindings[:-2] + ")"
        return statement

    def create_table_statement(self, table_name:str, schema:SQLSchema) -> str:
        statement = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for_keys = ""
        for col_name, sql_col in schema.schema_map.items():
            statement += f"{col_name} {self.__type_map[sql_col.data_type]}"
            if sql_col.is_primary_key:
                statement = statement + f" PRIMARY KEY"
            if not sql_col.nullable:
                statement = statement + f" NOT NULL"
            if sql_col.foreign_key:
                for_keys += f"FOREIGN KEY({col_name}) REFERENCES {sql_col.foreign_key['refences_table']} ({sql_col.foreign_key['references_col']}), "
            statement = statement + ", "
        if for_keys:
            statement += for_keys
        statement = statement[:-2] + f")"
        return statement
    