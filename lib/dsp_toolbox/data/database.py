import os
import logging
from typing import Optional
from enum import IntEnum, unique

import pandas as pd
import sqlite3


@unique
class DatabaseType(IntEnum):
    UNDEFINED = 0
    SQLITE = 1
    CSV = 2


class Database:

    def __init__(
        self,
        filepath: str,
        table_name: Optional[str] = None
    ):
        self.filepath: str = filepath
        self.database: pd.DataFrame
        self.db_type = self.identify_db_type()
        self.table_name = table_name
        
    def save_database(self) -> None:
        if not self.is_valid:
            logging.error("Cannot load database. Config invalid")
            return
        match self.db_type:
            case DatabaseType.SQLITE:
                self.save_sqlite()
            case DatabaseType.CSV:
                self.save_csv()
    
    def load_database(self) -> None:
        if not self.is_valid:
            logging.error("Cannot load database. Config invalid")
            return
        match self.db_type:
            case DatabaseType.SQLITE:
                self.load_sqlite()
            case DatabaseType.CSV:
                self.load_csv()

    def save_sqlite(self):
        with sqlite3.connect(self.filepath) as conn:
            self.database.to_sql(name=self.table_name, con=conn, if_exists='replace', index=False)
        logging.info(f"Saved frame to {self.filepath}")

    def load_sqlite(self) -> None:
        if not os.path.exists(self.filepath):
            logging.info("Cannot load table. Local SQLite file does not exist")
            self.database = pd.DataFrame()
            return
        sql = f"SELECT * FROM {self.table_name}"
        with sqlite3.connect(self.filepath) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if self.table_name not in tables:
                logging.error("Could not find table name")
                self.database = pd.DataFrame()
                return
            self.database = pd.read_sql(sql=sql, con=conn)
            
    def save_csv(self):
        self.database.to_csv(self.filepath, index=False)
        
    def load_csv(self):
        if not os.path.exists(self.filepath):
            logging.error(f"File {self.filepath} does not exist")
            self.database = pd.DataFrame()
            return
        self.database = pd.read_csv(self.filepath)
        
    def identify_db_type(self) -> DatabaseType:
        if self.filepath.endswith(".sqlite"):
            return DatabaseType.SQLITE
        if self.filepath.endswith(".csv"):
            return DatabaseType.CSV
        return DatabaseType.UNDEFINED
    
    @property
    def is_valid(self) -> bool:
        match self.db_type:
            case DatabaseType.UNDEFINED:
                return False
            case DatabaseType.SQLITE:
                return self.table_name is not None
            case DatabaseType.CSV:
                return True