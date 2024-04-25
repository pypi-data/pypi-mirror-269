import sqlexec as db
from orm.constant import KEY, UPDATE_BY, UPDATE_TIME, DEL_FLAG, KEY_SEQ, TABLE, KEY_STRATEGY
from .base import BaseGenerator

COMMON_COLS = ['create_by', 'create_time']
ATTRIBUTES = {KEY: 'id', UPDATE_BY: 'update_by', UPDATE_TIME: 'update_time', DEL_FLAG: 'del_flag'}


class PostgresqlGenerator(BaseGenerator):
    comma1 = ','
    comma2 = '，'
    sql = '''SELECT column_name as "COLUMN_NAME", udt_name as "DATA_TYPE", column_default 
             FROM information_schema.columns WHERE table_schema='public' AND table_name = ?'''
    key_sql = '''SELECT a.attname FROM pg_index i
                 JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = any(i.indkey)
                 WHERE i.indrelid = ?::regclass AND i.indisprimary LIMIT 1'''

    def __init__(self):
        super().__init__('postgresql.tpl', [KEY, KEY_SEQ, TABLE, UPDATE_BY, UPDATE_TIME, DEL_FLAG, KEY_STRATEGY])

    def _get_table_meta(self, table: str, base_columns):
        def convert_type(col_type):
            if col_type.startswith('int'):
                return 'int'
            elif col_type .startswith('float'):
                return 'float'
            elif col_type in('numeric'):
                return 'Decimal'
            elif col_type in ('char', 'varchar', 'text'):
                return 'str'
            elif col_type == 'timestamp':
                return 'datetime'
            elif col_type == 'date':
                return col_type
            else:
                return 'None'

        key, key_seq, super_columns = None, None, []
        columns = db.do_query(self.sql, table)
        for col in columns:
            if col['COLUMN_NAME'] in base_columns:
                super_columns.append(col)
            col['DATA_TYPE'] = convert_type(col['DATA_TYPE'])

            if col['column_default'] and col['column_default'].startswith('nextval('):
                key = col['COLUMN_NAME']
                key_seq = col['column_default'][9:-12]

        if key is None:
            key = db.do_get(self.key_sql, table)
            if key is None:
                return table

        class_name = self._get_class_name(table)
        return {
            'key': key,
            'key_seq': key_seq,
            'table': table,
            'class_name': class_name,
            'columns': columns,
            'self_columns': [col for col in columns if col['COLUMN_NAME'] not in base_columns],
            'super_columns': super_columns
        }

