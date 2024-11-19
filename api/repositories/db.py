import sqlite3
import logging
from contextlib import closing
from typing import Any, List, Tuple, Dict
import os


class Database:
    def __init__(self):
        self.db_file = os.getenv("DB_PATH")

    def _connect(self):
        """Establish a database connection."""
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logging.error(f"Database connection error: {e}")
            raise

    def _log_execution(
        self, sql: str, params: tuple, success: bool, result: Any = None
    ):
        """Log successful execution or errors."""
        if success:
            logging.info(
                f"Executed SQL: {sql} | Parameters: {params} | Result: {result}"
            )
        else:
            logging.error(
                f"Failed to execute SQL: {sql} | Parameters: {params} | Error: {result}"
            )

    def create(self, table: str, data: Dict[str, Any]) -> int:
        """Create a new record in the specified table."""
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?"] * len(data))
            sql = f"INSERT INTO [{table}] ({columns}) VALUES ({placeholders})"
            params = tuple(data.values())

            conn = self._connect()
            with closing(conn.cursor()) as cursor:
                cursor.execute(sql, params)
                conn.commit()
                self._log_execution(sql, params, success=True, result=cursor.lastrowid)
                return cursor.lastrowid  # Return the ID of the inserted row

        except sqlite3.Error as e:
            logging.error(f"Error in 'create' operation: {e}")
            conn.rollback()
            self._log_execution(sql, params, success=False, result=e)
            raise

        finally:
            conn.close()

    def read(self, sql: str, params: Dict = {}) -> List[Dict[str, Any]]:
        """Read records from the database."""
        try:
            conn = self._connect()
            with closing(conn.cursor()) as cursor:
                cursor.execute(sql, params)
                rows = cursor.fetchall()

                # Convert rows to a list of dictionaries, where each dictionary is a row
                results = [dict(row) for row in rows] if rows else []

                if len(results) == 1:
                    return results[0]

                self._log_execution(sql, params, success=True, result=results)
                return results

        except sqlite3.Error as e:
            logging.error(f"Error in 'read' operation: {e}")
            self._log_execution(sql, params, success=False, result=e)
            raise

        finally:
            conn.close()

    def update(
        self, table: str, data: Dict[str, Any], where: str, where_params: Tuple
    ) -> int:
        """Update existing records in the specified table."""
        try:
            set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
            sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
            params = tuple(data.values()) + where_params

            conn = self._connect()
            with closing(conn.cursor()) as cursor:
                cursor.execute(sql, params)
                conn.commit()
                self._log_execution(sql, params, success=True, result=cursor.rowcount)
                return cursor.rowcount  # Return number of rows affected

        except sqlite3.Error as e:
            logging.error(f"Error in 'update' operation: {e}")
            conn.rollback()
            self._log_execution(sql, params, success=False, result=e)
            raise

        finally:
            conn.close()

    def delete(self, table: str, where: str, where_params: Tuple) -> int:
        """Delete records from the specified table."""
        try:
            sql = f"DELETE FROM [{table}] WHERE {where}"
            conn = self._connect()
            with closing(conn.cursor()) as cursor:
                cursor.execute(sql, where_params)
                conn.commit()
                self._log_execution(
                    sql, where_params, success=True, result=cursor.rowcount
                )
                return cursor.rowcount

        except sqlite3.Error as e:
            logging.error(f"Error in 'delete' operation: {e}")
            conn.rollback()
            self._log_execution(sql, where_params, success=False, result=e)
            raise

        finally:
            conn.close()

    def execute_sql(self, sql: str, params: Tuple = ()) -> Any:
        """Execute arbitrary SQL (e.g., for SELECT or other complex queries)."""
        try:
            conn = self._connect()
            with closing(conn.cursor()) as cursor:
                cursor.execute(sql, params)
                if sql.strip().lower().startswith("select"):
                    rows = cursor.fetchall()
                    # Convert rows to a list of dictionaries, where each dictionary is a row
                    results = [dict(row) for row in rows] if rows else []
                    self._log_execution(sql, params, success=True, result=results)
                    return results
                else:
                    conn.commit()
                    self._log_execution(
                        sql, params, success=True, result=cursor.rowcount
                    )
                    return (
                        cursor.rowcount
                    )  # Return number of rows affected for non-SELECT queries

        except sqlite3.Error as e:
            logging.error(f"Error in 'execute_sql' operation: {e}")
            conn.rollback()
            self._log_execution(sql, params, success=False, result=e)
            raise

        finally:
            conn.close()
