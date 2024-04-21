from typing import Protocol, Literal
import psycopg2
from .schema_objects import SQLSchema, SQLColumn

ALTER_COL_OP = Literal["DROP", "ADD", "ALTER", "RENAME COLUMN", "RENAME TABLE"]
DB_TYPE_LIST = Literal["integer", "smallint", "bigint", "real", "double precision", "decimal", "numeric", "text", 
                         "timestamp with time zone", "timestamp", "date", "time with time zone", "time", "interval", 
                         "uuid", "json", "jsonb", "geometry"]

class Database(Protocol):

    @property
    def db_conn(self) -> psycopg2.extensions.connection:
        ...

    def table_from_records(self, table_name:str, table_records:list[dict], col_overrides:list[SQLColumn]=[], schema_override:SQLSchema=None, postgresql_schema:str="public") -> None:
        ...

    def table_append_records(self, table_name:str, table_records:list[dict[str]], postgresql_schema:str="public") -> None:
        ...
    
    def update_with_unique_records(self, table_name:str, records:list[dict], unique_key_col:str, postgresql_schema:str="public") -> None:
        ...

    def delete_rows(self, table_name:str, where_clause:str, postgresql_schema:str="public") -> None:
        ...

    def append_csv_to_table(self, table_name:str, csv_path:str) -> None:
        ...
    
    def records_to_csv(self, csv_name:str, csv_path:str) -> None:
        ...

    def create_blank_table(self, table_name:str, schema:SQLSchema, postgresql_schema:str="public") -> None:
        ...
    
    def csv_to_records(self, csv_path:str) -> list[dict]:
        ...

    def csv_to_table(self, csv_path:str, col_overrides:list[SQLColumn]=[], schema_override:SQLSchema=None, postgresql_schema:str = "public") -> None:
        ...

    def table_to_records(self, table_name:str, columns:str="*", where_clause:str="", postgresql_schema:str="public") -> list[dict]:
        ...
    
    def table_to_csv(self, table_name:str, save_path:str=".", columns:str="*", where_clause:str="", postgresql_schema:str="public") -> None:
        ...

    def drop_table(self, table_name:str) -> None:
        ...
    
    def delete_all_records(self, table_name:str, postgresql_schema:str="public") -> None:
        ...

    def add_column(self, table_name:str, col_name:str, data_type:DB_TYPE_LIST, postgresql_schema:str="public") -> None:
        ...
    
    def drop_column(self, table_name:str, col_name:str, postgresql_schema:str="public") -> None:
        ...
    
    def rename_column(self, table_name:str, col_name:str, new_col_name:str, postgresql_schema:str="public") -> None:
        ...

    def rename_table(self, table_name:str, new_table_name:str, postgresql_schema:str="public") -> None:
        ...

    def list_tables(self, postgresql_schema:str="public") -> list[str]:
        ...

    def get_schema(self, table_name:str, postgresql_schema:str="public") -> SQLSchema:
        ...

    def get_table(self, table_name:str, columns:str="*", where_clause:str="", postgresql_schema:str="public") -> list[tuple]:
        ...

    def evaluate_schema(self, records:list[dict], col_overrides:list[SQLColumn]=[]) -> SQLSchema:
        ...

    def select_table_statement(self, table_name:str, columns:str="*", where_clause:str="") -> str:
        ...

    def create_update_statement(self, table_name:str, record_row:dict, where_clause:str) -> str:
        ...

    def create_delete_statement(self, table_name:str, where_clause:str) -> str:
        ...

    def insert_into_table_statement(self, table_name:str, schema:SQLSchema) -> str:
        ...

    def create_table_statement(self, table_name:str, schema:SQLSchema) -> str:
        ...

    def infer_type(self, val:str) -> str:
        ...






