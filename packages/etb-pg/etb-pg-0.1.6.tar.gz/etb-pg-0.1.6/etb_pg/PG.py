"""Small psycopg wrapper."""

from typing import Any, Callable
import psycopg


class PGDB:
    '''class for interacting with Postgres Databases\n
    conn_dict: dict = {
        "user" : "",
        "password" : "",
        "host" : "",
        "port" : "",
        "dbname" : ""
    }
    read_only (optional, default=True): Set the connection to be read only\n
    sql_dir (optional): Specify the absolute path of the directory where queries are stored\n
    README at https://github.com/HFxLhT8JqeU5BnUG/etb-pg'''

    DEFAULT_SCHEMA: str = "public"

    def __init__(self, conn_dict: dict[str, str],
                 read_only: bool = True, sql_dir: str = ""):

        self.__connection__: psycopg.Connection = psycopg.connect(**conn_dict)
        self.__connection__.read_only = read_only

        if sql_dir and not sql_dir.endswith('/'):
            sql_dir += '/'

        self.__SQL_DIR__ = sql_dir


    def execute_file_query(self, file_name: str):
        '''Executes the first query found in the specified file\n
        If no file extension is included in the file_name, it is assumed that it is a .sql file\n
        This will search the sql_dir set when object is instantiated. If no SQL directory was set,
        then it will assume that file_name is an absolute path'''

        if '.' not in file_name:
            file_name += '.sql'

        if self.__SQL_DIR__:
            location = self.__SQL_DIR__ + file_name
        else:
            location = file_name

        with open(location) as file:
            query = file.read()

        return self._execute_query(query)


    def execute_str_query(self, query: str):
        '''Execute a raw string query'''
        return self._execute_query(query)


    def _execute_query(self, query: str) -> list[dict[str, Any]] | None:
        '''Internal use, called by class methods that accept various input formats'''

        with self.__connection__.cursor() as curs:

            curs.execute(query)
            if not curs.description:
                self.__connection__.commit()
                return

            else:
                result = curs.fetchall()
                cols = curs.description

                rows = [
                    { cols[i].name : row[i] for i in range(len(row)) }
                    for row in result
                    ]

                return rows


    def str_to_query(self, fun: Callable[..., str]):
        '''Decorator for function that returns a string\n
        Will treat the string returned by decorated function as a query and return the result'''

        def wrapper(*args, **kwargs):
            query = fun(*args, **kwargs)
            assert isinstance(query, str), \
                f'Decorated function must return a string, not {type(query)}'

            return self.execute_str_query(query)

        return wrapper


    def get_columns(self, table_name: str, schema: str = DEFAULT_SCHEMA) -> dict[str, Any]:
        '''Pass the name of the table, and (optional) the schema\n
        Returns names and types of rows as dictionary'''
        location = schema + "." + table_name

        query = f"select * from {location} limit 1;"

        row = self._execute_query(query)[0]

        return {key: type(value) for key, value in row.items()}


    def get_rows(self, table_name: str, schema: str = DEFAULT_SCHEMA, cols: list[str] = None):
        '''Select specified columns from a table\n
        schema (optional, defaults to public)\n
        cols (optional, defaults to "*")'''

        if not cols:
            select_cols = '*'
        else:
            select_cols = ', '.join(cols)

        location = schema + "." + table_name

        query = f"select {select_cols} from {location};"

        return self._execute_query(query)
