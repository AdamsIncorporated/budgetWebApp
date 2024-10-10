import sqlite3
import logging
from sqlite3 import Error
import os
from dotenv import load_dotenv

class DatabaseManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_connection(self):
        conn = None
        try:
            load_dotenv()
            path = os.environ.get("DB_PATH")
            conn = sqlite3.connect(path)
            self.logger.info(f"Connection to SQLite DB '{path}' successful.")
        except Error as e:
            self.logger.error(f"Error '{e}' occurred while connecting to the database.")
            raise Exception(f"Error '{e}' occurred while connecting to the database.")

        return conn

    def execute_query(self, query, params=None):
        try:
            connection = self.create_connection()  # Create a new connection
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            self.logger.info("Query executed successfully.")
        except Error as e:
            self.logger.error(
                f"Error '{e}' occurred while executing the query: {query} with params: {params}"
            )
            raise Exception(f"Error '{e}' occurred while executing the query.")
        finally:
            if connection:
                connection.close()  # Ensure the connection is closed

    def fetch_all(self, query, params=None):
        try:
            connection = self.create_connection()  # Create a new connection
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            column_headers = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            combined_results = [dict(zip(column_headers, row)) for row in results]
            self.logger.info(f"Fetched {len(results)} records successfully.")
            return combined_results
        except Error as e:
            self.logger.error(
                f"Error '{e}' occurred while fetching data with query: {query} and params: {params}"
            )
            raise Exception(f"Error '{e}' occurred while fetching data.")
        finally:
            if connection:
                connection.close()  # Ensure the connection is closed

    def insert(self, table_name, data):
        placeholders = ", ".join("?" * len(data))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
        self.execute_query(insert_query, data)
        self.logger.info(f"Inserted data into {table_name}: {data}")

    def update(self, table_name, data, condition):
        set_clause = ", ".join(f"{k} = ?" for k in data.keys())
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition};"
        self.execute_query(update_query, list(data.values()))
        self.logger.info(f"Updated {table_name} set {data} where {condition}")

    def delete(self, table_name, condition):
        delete_query = f"DELETE FROM {table_name} WHERE {condition};"
        self.execute_query(delete_query)
        self.logger.info(f"Deleted from {table_name} where {condition}")
