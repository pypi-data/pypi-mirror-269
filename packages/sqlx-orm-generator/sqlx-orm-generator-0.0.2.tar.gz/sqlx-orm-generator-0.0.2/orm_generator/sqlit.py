import sqlexec as db
from orm.constant import KEY, UPDATE_BY, UPDATE_TIME, DEL_FLAG

from .base import BaseGenerator

COMMON_COLS = ['create_by', 'create_time']
ATTRIBUTES = {KEY: 'id', UPDATE_BY: 'update_by', UPDATE_TIME: 'update_time', DEL_FLAG: 'del_flag'}


class SqliteGenerator(BaseGenerator):
    comma1 = ','
    comma2 = '，'
    sql = 'PRAGMA table_info(%s)'

    def __init__(self):
        super().__init__('mysql.tpl')

    def _get_table_meta(self, table: str, base_columns):
        def convert_type(col_type):
            if col_type in ('int', 'tinyint', 'bigint', 'INTEGER', 'smallint'):
                return 'int'
            elif col_type in ('float', 'double'):
                return 'float'
            elif 'decimal' in col_type:
                return 'Decimal'
            elif col_type in ('char', 'varchar', 'TEXT'):
                return 'str'
            elif col_type in ('date', 'datetime'):
                return col_type
            elif col_type == 'timestamp':
                return 'datetime'
            else:
                return 'None'

        key = None
        super_columns = []
        columns = db.do_query(self.sql % table)
        for col in columns:
            if col['pk'] == 1:
                key = col['name']
            if col['name'] in base_columns:
                super_columns.append(col)
            col['DATA_TYPE'] = convert_type(col['type'])
            col['COLUMN_NAME'] = col['name']

        if key is None:
            return table

        class_name = self._get_class_name(table)
        return {
            'key': key,
            'table': table,
            'class_name': class_name,
            'columns': columns,
            'self_columns': [col for col in columns if col['name'] not in base_columns],
            'super_columns': super_columns
        }
