import json
from typing import Literal
from .postgres_interface import PostgreSQL
from .schema_objects import SQLColumn, SQLSchema



ALTER_COL_OP = Literal["DROP", "ADD", "ALTER", "RENAME COLUMN", "RENAME TABLE"]
POSTGIS_TYPES = Literal["integer", "smallint", "bigint", "real", "double precision", "decimal", "numeric", "smallserial", 
                        "serial", "bigserial", "text", "timestamp with time zone", "timestamp", "date", "time with time zone", 
                        "time", "interval", "uuid", "json", "jsonb", "geometry", "boolean"]

POSTGIS_TYPE_MAP = {"integer": "integer", "smallint": "smallint", "bigint": "bigint", 
                    "real": "real", "double precision": "double precision", "decimal": "decimal", "numeric": "numeric", 
                    "smallserial": "smallserial", "serial": "serial", "bigserial": "bigserial", "geometry": "geometry", "text": "text", 
                    "timestamp": "timestamp", "timestamp with time zone": "timestamp with time zone", "boolean": "boolean",
                    "date": "date", "time with time zone": "time with time zone", "time": "time", "interval": "interval",
                    "uuid": "uuid DEFAULT gen_random_uuid()", "json": "json", "jsonb": "jsonb"}

class PostGIS(PostgreSQL):
    def __init__(self, db_name: str, username: str, password: str, host="localhost", port=5432, type_map=POSTGIS_TYPE_MAP):
        super().__init__(db_name, username, password, host, port, type_map)


