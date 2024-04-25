import sqlexec as db
from orm.constant import KEY, UPDATE_BY, UPDATE_TIME, DEL_FLAG

from .base import BaseGenerator

COMMON_COLS = ['create_by', 'create_time']
ATTRIBUTES = {KEY: 'id', UPDATE_BY: 'update_by', UPDATE_TIME: 'update_time', DEL_FLAG: 'del_flag'}


class MySQLGenerator(BaseGenerator):
    comma1 = ','
    comma2 = '，'
    sql = '''
    SELECT column_name, data_type, character_maximum_length, NUMERIC_precision, NUMERIC_scale, column_key FROM information_schema.columns
     WHERE table_schema = (SELECT DATABASE()) AND table_name = ? 
    '''

    def __init__(self):
        super().__init__('mysql.tpl')

    def _get_table_meta(self, table: str, base_columns):
        def convert_type(col_type):
            if col_type in ('int', 'tinyint', 'bigint'):
                return 'int'
            elif col_type in ('float', 'double'):
                return 'float'
            elif col_type == 'decimal':
                return 'Decimal'
            elif col_type in ('char', 'varchar', 'text'):
                return 'str'
            elif col_type in ('date', 'datetime'):
                return col_type
            else:
                return 'None'

        key = None
        super_columns = []
        columns = db.do_query(self.sql, table)
        for col in columns:
            if col['COLUMN_KEY'] == 'PRI':
                key = col['COLUMN_NAME']
            if col['COLUMN_NAME'] in base_columns:
                super_columns.append(col)
            col['DATA_TYPE'] = convert_type(col['DATA_TYPE'])

        if key is None:
            return table

        class_name = self._get_class_name(table)
        return {
            'key': key,
            'table': table,
            'class_name': class_name,
            'columns': columns,
            'self_columns': [col for col in columns if col['COLUMN_NAME'] not in base_columns],
            'super_columns': super_columns
        }
