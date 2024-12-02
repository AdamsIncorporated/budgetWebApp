import psycopg2
import logging
from contextlib import closing
from typing import Any, List, Tuple, Dict
import os


class Database:
    def __init__(self):
        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")

    def _connect(self):
        """Establish a database connection."""
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            conn.autocommit = False  # Disable autocommit to control transactions
            return conn
        except psycopg2.Error as e:
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
            placeholders = ", ".join(["%s"] * len(data))
            sql = f'INSERT INTO "{table}" ({columns}) VALUES ({placeholders}) RETURNING id'
            params = tuple(data.values())

            conn = self._connect()
            with closing(conn.cursor()) as cursor:
                cursor.execute(sql, params)
                conn.commit()
                new_id = cursor.fetchone()[0]  # Get the returned ID
                self._log_execution(sql, params, success=True, result=new_id)
                return new_id

        except psycopg2.Error as e:
            logging.error(f"Error in 'create' operation: {e}")
            conn.rollback()
            self._log_execution(sql, params, success=False, result=e)
            raise

        finally:
            conn.close()

    def read(
        self, sql: str, params: Tuple = ()
    ) -> List[Dict[str, Any]] | Dict[str, Any]:
        """Read records from the database."""
        try:
            conn = self._connect()
            with closing(conn.cursor()) as cursor:
                cursor.execute(sql, params)
                rows = cursor.fetchall()

                # Convert rows to a list of dictionaries
                if rows:
                    if len(rows) == 1:
                        # If there is exactly one row, return it as a dictionary
                        results = dict(
                            zip([desc[0] for desc in cursor.description], rows[0])
                        )
                    else:
                        # Otherwise, return as a list of dictionaries
                        results = [
                            dict(zip([desc[0] for desc in cursor.description], row))
                            for row in rows
                        ]
                else:
                    results = []

                self._log_execution(sql, params, success=True, result=results)
                return results

        except psycopg2.Error as e:
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
            set_clause = ", ".join([f"{col} = %s" for col in data.keys()])
            sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
            params = tuple(data.values()) + where_params

            conn = self._connect()
            with closing(conn.cursor()) as cursor:
                cursor.execute(sql, params)
                conn.commit()
                rowcount = cursor.rowcount
                self._log_execution(sql, params, success=True, result=rowcount)
                return rowcount

        except psycopg2.Error as e:
            logging.error(f"Error in 'update' operation: {e}")
            conn.rollback()
            self._log_execution(sql, params, success=False, result=e)
            raise

        finally:
            conn.close()

    def delete(self, table: str, where: str, where_params: Tuple) -> int:
        """Delete records from the specified table."""
        try:
            sql = f"DELETE FROM {table} WHERE {where}"
            conn = self._connect()
            with closing(conn.cursor()) as cursor:
                cursor.execute(sql, where_params)
                conn.commit()
                rowcount = cursor.rowcount
                self._log_execution(sql, where_params, success=True, result=rowcount)
                return rowcount

        except psycopg2.Error as e:
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
                    results = (
                        [
                            dict(zip([desc[0] for desc in cursor.description], row))
                            for row in rows
                        ]
                        if rows
                        else []
                    )
                    self._log_execution(sql, params, success=True, result=results)
                    return results
                else:
                    conn.commit()
                    rowcount = cursor.rowcount
                    self._log_execution(sql, params, success=True, result=rowcount)
                    return rowcount

        except psycopg2.Error as e:
            logging.error(f"Error in 'execute_sql' operation: {e}")
            conn.rollback()
            self._log_execution(sql, params, success=False, result=e)
            raise

        finally:
            conn.close()
