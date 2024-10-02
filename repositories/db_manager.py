import sqlite3
import logging
from sqlite3 import Error


class DatabaseManager:
    def __init__(self, db_file, logger=None):
        """Initialize the DatabaseManager with a database file and a logger."""
        self.logger = logger or logging.getLogger(__name__)
        self.connection = self.create_connection(db_file)

    def create_connection(self, db_file):
        """Create a database connection to the SQLite database."""
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            self.logger.info(f"Connection to SQLite DB '{db_file}' successful.")
        except Error as e:
            self.logger.error(f"Error '{e}' occurred while connecting to the database.")
            raise Exception(f"Error '{e}' occurred while connecting to the database.")

        return conn

    def execute_query(self, query, params=None):
        """Execute a single query with optional parameters."""
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            self.logger.info("Query executed successfully.")
        except Error as e:
            self.logger.error(
                f"Error '{e}' occurred while executing the query: {query} with params: {params}"
            )
            raise Exception(f"Error '{e}' occurred while executing the query.")

    def fetch_all(self, query, params=None):
        """Fetch all results from a query."""
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            self.logger.info(f"Fetched {len(results)} records successfully.")
            return results
        except Error as e:
            self.logger.error(
                f"Error '{e}' occurred while fetching data with query: {query} and params: {params}"
            )
            raise Exception(f"Error '{e}' occurred while fetching data.")

    def insert(self, table_name, data):
        """Insert a new record into the specified table."""
        placeholders = ", ".join("?" * len(data))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
        self.execute_query(insert_query, data)
        self.logger.info(f"Inserted data into {table_name}: {data}")

    def update(self, table_name, data, condition):
        """Update records in the specified table based on the condition."""
        set_clause = ", ".join(f"{k} = ?" for k in data.keys())
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition};"
        self.execute_query(update_query, list(data.values()))
        self.logger.info(f"Updated {table_name} set {data} where {condition}")

    def delete(self, table_name, condition):
        """Delete records from the specified table based on the condition."""
        delete_query = f"DELETE FROM {table_name} WHERE {condition};"
        self.execute_query(delete_query)
        self.logger.info(f"Deleted from {table_name} where {condition}")

    def close_connection(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.logger.info("Connection to SQLite DB closed.")
