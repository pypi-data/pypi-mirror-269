import sqlexec
from sqlexec.dialect import Engine
from typing import Union, Iterable

class Generator:

    def __init__(self, *args, **kwargs):
        """
        Compliant with the Python DB API 2.0 (PEP-249).

        from mysqlx.generator import Generator
        coder = Generator("postgres://user:password@127.0.0.1:5432/testdb", driver='psycopg2')
        or
        coder = Generator(user='root', password='xxx', host='127.0.0.1', port=3306, database='testdb', driver='pymysql')

        Addition parameters:
        :param driver: str, import driver, 'import pymysql'
        :param pool_size: int, size of connection pool
        :param show_sql: bool, if True, print sql
        :param debug: bool, if True, print debug context

        Other parameters of connection pool refer to DBUtils: https://webwareforpython.github.io/DBUtils/main.html#pooleddb-pooled-db
        """
        engine = sqlexec.init(*args, **kwargs)
        if Engine.MYSQL == engine:
            from .mysql import MySQLGenerator
            self.generator = MySQLGenerator()
        elif Engine.POSTGRESQL == engine:
            from .postgresql import PostgresqlGenerator
            self.generator = PostgresqlGenerator()
        elif Engine.SQLITE == engine:
            from .sqlit import SqliteGenerator
            self.generator = SqliteGenerator()
        else:
            raise NotImplementedError(f'Not implemented for {engine.value}')

    def generate_with_schema(self, schema: str = None, path: str = None, *args, **kwargs):
        self.generator.generate_with_schema(schema, path, *args, **kwargs)

    def generate_with_tables(self, tables: Union[str, Iterable[str]], path: str = None, *args, **kwargs):
        self.generator.generate_with_tables(tables, path, *args, **kwargs)
