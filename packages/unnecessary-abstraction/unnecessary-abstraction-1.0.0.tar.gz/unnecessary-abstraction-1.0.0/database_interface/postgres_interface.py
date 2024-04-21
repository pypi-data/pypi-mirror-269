from .database import Database
from typing import Literal
import psycopg2
import pathlib
import json
import csv

from .schema_objects import SQLColumn, SQLSchema

TABLE_ACTION = Literal["INSERT", "UPDATE", "DELETE"]
FOR_EACH = Literal["ROW", "STATEMENT"]

POSTGRES_TYPES = Literal["integer", "smallint", "bigint", "real", "double precision", "decimal", "numeric", "text", 
                         "timestamp with time zone", "timestamp", "date", "time with time zone", "time", "interval", 
                         "uuid", "json", "jsonb", "boolean"]
POSTGRES_TYPE_MAP = {"integer": "integer", "smallint": "smallint", "bigint": "bigint", 
                     "real": "real", "double precision": "double precision", "decimal": "decimal", "numeric": "numeric", 
                     "smallserial": "smallserial", "serial": "serial", "bigserial": "bigserial", "geometry": "text", "text": "text", 
                     "timestamp": "timestamp", "timestamp with time zone": "timestamp with time zone", "boolean": "boolean",
                     "date": "date", "time with time zone": "time with time zone", "time": "time", "interval": "interval",
                     "uuid": "uuid DEFAULT gen_random_uuid()", "json": "json", "jsonb": "jsonb"}

class PostgreSQL(Database):
    def __init__(self, db_name:str, username:str, password:str, host="localhost", port=5432, type_map=POSTGRES_TYPE_MAP):
        self.__db_conn = psycopg2.connect(database=db_name, user=username, password=password, host=host, port=port)
        self.__binding_char = "%s"
        self.__type_map = type_map

    @property
    def db_conn(self):
        return self.__db_conn

    def table_from_records(self, table_name:str, table_records:list[dict], col_overrides:list[SQLColumn]=[], schema_override:SQLSchema=None, postgresql_schema:str="public") -> None:
        schema:SQLSchema = schema_override
        if not schema_override:
            schema = self.evaluate_schema(table_records, col_overrides)

        create_statement = self.create_table_statement(f"{postgresql_schema}.{table_name}", schema)
        insert_statement = self.insert_into_table_statement(f"{postgresql_schema}.{table_name}", schema)
        table_records_sql = [tuple(val for val in row.values()) for row in table_records]

        cur = self.db_conn.cursor()
        cur.execute(create_statement)
        cur.executemany(insert_statement, table_records_sql)
        self.db_conn.commit()

    def table_append_records(self, table_name:str, table_records:list[dict[str]], postgresql_schema:str="public") -> None:
        schema = self.get_schema(table_name, postgresql_schema)
        schema.filter_columns(list(table_records[0].keys()))
        
        insert_statement = self.insert_into_table_statement(f"{postgresql_schema}.{table_name}", schema)
        table_records_sql = [tuple(val for val in row.values()) for row in table_records]

        cur = self.db_conn.cursor()
        cur.executemany(insert_statement, table_records_sql)
        self.db_conn.commit()

    def update_with_unique_records(self, table_name:str, records:list[dict], unique_key_col:str, postgresql_schema:str="public") -> None:
        cur = self.db_conn.cursor()
        for row in records:
            update_statement = self.create_update_statement(f"{postgresql_schema}.{table_name}", row, f"WHERE {unique_key_col}='{row[unique_key_col]}'")
            cur.execute(update_statement)
        self.db_conn.commit()

    def delete_rows(self, table_name:str, where_clause:str, postgresql_schema:str="public") -> None:
        cur = self.db_conn.cursor()
        delete_statement = self.create_delete_statement(f"{postgresql_schema}.{table_name}", where_clause)
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

    def create_blank_table(self, table_name:str, schema:SQLSchema, postgresql_schema:str="public") -> None:
        sql = self.create_table_statement(f"{postgresql_schema}.{table_name}", schema)
        cur = self.db_conn.cursor()
        cur.execute(sql)
        self.db_conn.commit()
        
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
    
    def csv_to_table(self, csv_path:str, col_overrides:list[SQLColumn]=[], schema_override:SQLSchema=None, postgresql_schema:str = "public") -> None:
        csv_name = pathlib.Path(csv_path).stem
        records = self.csv_to_records(csv_path)
        if csv_name in self.list_tables():
            print(f"{csv_name} is already a table in the database. You can alternatively use append_csv() if this is intended")
            return
        self.table_from_records(csv_name, records, col_overrides, schema_override, postgresql_schema)

    def table_to_records(self, table_name:str, columns:str="*", where_clause:str="", postgresql_schema:str="public") -> list[dict]:
        schema:SQLSchema = self.get_schema(table_name, postgresql_schema)
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

    def table_to_csv(self, table_name:str, save_path:str=".", columns:str="*", where_clause:str="", postgresql_schema:str="public") -> None:
        table_records = self.table_to_records(table_name, columns, where_clause, postgresql_schema)
        headers:dict = table_records[0]
        headers = headers.keys()

        with open(f"{save_path}\\{table_name}.csv", 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(table_records)
    
    def drop_table(self, table_name:str) -> None:
        cur = self.db_conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.db_conn.commit()
    
    def delete_all_records(self, table_name:str, postgresql_schema:str="public") -> None:
        cur = self.db_conn.cursor()
        cur.execute(f"DELETE FROM {postgresql_schema}.{table_name}")
        self.db_conn.commit()

    def add_column(self, table_name:str, col_name:str, data_type:POSTGRES_TYPES, postgresql_schema:str="public") -> None:
        cur = self.db_conn.cursor()
        sql_statement = f"ALTER TABLE {postgresql_schema}.{table_name} ADD {col_name} {self.__type_map[data_type]}"
        cur.execute(sql_statement)
        self.db_conn.commit()
    
    def drop_column(self, table_name:str, col_name:str, postgresql_schema:str="public") -> None:
        cur = self.db_conn.cursor()
        sql_statement = f"ALTER TABLE {postgresql_schema}.{table_name} DROP COLUMN {col_name}"
        cur.execute(sql_statement)
        self.db_conn.commit()
    
    def rename_column(self, table_name:str, col_name:str, new_col_name:str, postgresql_schema:str="public") -> None:
        cur = self.db_conn.cursor()
        sql_statement = f"ALTER TABLE {postgresql_schema}.{table_name} RENAME COLUMN {col_name} TO {new_col_name}"
        cur.execute(sql_statement)
        self.db_conn.commit()

    def rename_table(self, table_name:str, new_table_name:str, postgresql_schema:str="public") -> None:
        cur = self.db_conn.cursor()
        sql_statement = f"ALTER TABLE {postgresql_schema}.{table_name} RENAME TO {new_table_name}"
        cur.execute(sql_statement)
        self.db_conn.commit()

    def alter_column(self, table_name:str, col_name:str, data_type:POSTGRES_TYPES, postgresql_schema:str="public") -> None:
        cur = self.db_conn.cursor()
        sql_statement = f"ALTER TABLE {postgresql_schema}.{table_name} ALTER COLUMN {col_name} {self.__type_map[data_type]}"
        cur.execute(sql_statement)
        self.db_conn.commit()

    def create_trigger_function(self, function_name:str, function_sql:str) -> None:
        create_function = f"CREATE OR REPLACE FUNCTION {function_name}() RETURNS trigger AS $$"
        create_function += f"BEGIN {function_sql}"
        create_function += "END; $$ LANGUAGE plpgsql;"

        cur = self.db_conn.cursor()
        cur.execute(create_function)
        self.db_conn.commit()

    def create_trigger(self, trigger_name:str, after_action:TABLE_ACTION, for_each:FOR_EACH, table_name:str, call_function:str) -> None:
        trigger_sql = f"CREATE TRIGGER {trigger_name}"
        trigger_sql += f"AFTER {after_action} ON {table_name}"
        trigger_sql += f"FOR EACH {for_each} EXECUTE FUNCTION {call_function}();"

        cur = self.db_conn.cursor()
        cur.execute(trigger_sql)
        self.db_conn.commit()

    def list_tables(self, postgresql_schema:str="public") -> list[str]:
        cur = self.db_conn.cursor()
        sql = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{postgresql_schema}'"
        cur.execute(sql)
        return [table[0] for table in cur.fetchall()]

    def get_schema(self, table_name:str, postgresql_schema:str="public") -> SQLSchema:
        GET_COL_SCHEMA = f"SELECT column_name, data_type, ordinal_position, is_nullable FROM information_schema.columns WHERE table_schema='{postgresql_schema}' AND table_name='{table_name}'"
        cur = self.db_conn.cursor()
        cur.execute(GET_COL_SCHEMA)
        col_list = []
        for col in cur.fetchall():
            if col[3] == 'YES':
                nullable = True
            else:
                nullable = False
            col_list.append(SQLColumn(col[0], col[1], col[2], nullable))

        schema = SQLSchema(col_list)
        return schema
    
    def get_table(self, table_name:str, columns:str="*", where_clause:str="", postgresql_schema:str="public") -> list[tuple]:
        select_statement = self.select_table_statement(f"{postgresql_schema}.{table_name}", columns, where_clause)
        cur = self.db_conn.cursor()
        cur.execute(select_statement)
        return cur.fetchall()

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
                                        is_primary_key=col.is_primary_key, foreign_key=col.foreign_key, 
                                        is_unique=col.is_unique, check_constraint=col.check_constraint,
                                        not_null=col.nullable))
            else:
                if col_val:
                    d_type = self.infer_type(col_val)
                else:
                    d_type = self.infer_type(find_non_null_record(records, col_name))
                
                schema.append(SQLColumn(name=col_name, data_type=d_type, position=pos))
            pos += 1
        return SQLColumn(schema)

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
            if sql_col.is_unique and not sql_col.is_primary_key:
                statement = statement + f" UNIQUE"
            if not sql_col.nullable and not sql_col.is_primary_key:
                statement = statement + f" NOT NULL"
            if sql_col.check_constraint:
                statement = statement + f" {sql_col.check_constraint}"
            if sql_col.foreign_key:
                statement = statement + f" REFERENCES {sql_col.foreign_key['refences_table']} ({sql_col.foreign_key['references_col']})"
            statement = statement + ", "
        if for_keys:
            statement += for_keys
        statement = statement[:-2] + f")"
        return statement

    def infer_type(self, val:str) -> str:

        def string_jsonable(x):
            try:
                json.loads(x)
                return True
            except (TypeError, OverflowError, json.decoder.JSONDecodeError):
                return False
        def dict_jsonable(x):
            try:
                json.dumps(x)
                return True
            except (TypeError, OverflowError, json.decoder.JSONDecodeError):
                return False

        if string_jsonable(val):
            return "json"
        elif type(val) == dict and dict_jsonable(val):
            return "json"

        if type(val) == int or type(val) == float:
            if type(val) == int:
                return "integer"
            elif type(val) == float:
                return "decimal"
        elif type(val) == bool:
            return "text"
        else:
            val:str
            split = val.split(".")
            if len(split) == 2:
                if split[0].isnumeric() and split[1].isnumeric():
                    if len(split[1]) > 8:
                        return "double precision"
                    else:
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

