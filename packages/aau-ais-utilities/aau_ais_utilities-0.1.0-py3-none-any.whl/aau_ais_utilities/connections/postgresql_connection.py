"""PostgreSQLConnection class to run sql queries on a given SQL database."""
from sqlalchemy import text, Engine, CursorResult
from sqlalchemy.orm import sessionmaker
from pathlib import Path


class PostgreSQLConnection:
    """Run sql queries on a given SQL database."""

    def __init__(self, engine: Engine) -> None:
        """Initialize the SQLRunner class.

        Args:
            engine: The sqlalchemy engine to use for connecting to the SQL database.
        """
        self.engine = engine
        self.session = sessionmaker(bind=self.engine)

    def execute_sql(self, *, sql: str | Path, params: dict = None) -> CursorResult:
        """Execute SQL query on the database.

        Args:
            sql: The sql query to run or the path to a file containing the query.
            params: A dictionary of parameters to pass to the sql query. Defaults to None.
        """
        if isinstance(sql, Path):
            with open(sql, 'r') as sql_file:
                sql = sql_file.read()

        if not isinstance(sql, str):
            raise ValueError('The sql query must be a string or a path to a file containing the query.')

        return self._executing_session(text(sql), params)

    def _executing_session(self, query: text, params: dict = None) -> CursorResult:
        """Execute SQL query on the database.

        Args:
            query: The sql query to run.
            params: A dictionary of parameters to pass to the sql query. Defaults to None.
        """
        session = self.session()

        try:
            result = session.connection().execute(query, params)
            session.commit()

        except Exception as e:
            raise e

        finally:
            session.close()

        return result
