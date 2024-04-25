import os
import sqlexec as db
from typing import Union, Iterable
from jinja2 import FileSystemLoader, Environment
from orm.constant import KEY, TABLE, UPDATE_BY, UPDATE_TIME, DEL_FLAG, KEY_STRATEGY

COMMON_COLS = ['create_by', 'create_time']
ATTRIBUTES = {KEY: 'id', UPDATE_BY: 'update_by', UPDATE_TIME: 'update_time', DEL_FLAG: 'del_flag'}


class BaseGenerator:

    def __init__(self, template: str, attribute_list=None):
        self.template = template
        self.attribute_list = attribute_list if attribute_list else [KEY, TABLE, UPDATE_BY, UPDATE_TIME, DEL_FLAG, KEY_STRATEGY]

    def generate_with_schema(self, schema: str = None, path: str = None, *args, **kwargs):
        """
        coder = Generator(user='root', password='xxx', host='127.0.0.1', port=3306, database='testdb', driver='pymysql')
        coder.generate_with_schema('testdb', 'models.py')
        """

        tables = db.show_tables(schema)
        self.generate_with_tables(tables=tables, path=path, *args, **kwargs)

    def generate_with_tables(self, tables: Union[str, Iterable[str]], path: str = None, *args, **kwargs):
        """
        coder = Generator(user='root', password='xxx', host='127.0.0.1', port=3306, database='testdb', driver='pymysql')
        coder.generate_with_tables(['user', 'person'], 'models.py')
        """

        metas = None
        only_one_table = False
        if not args:
            args = COMMON_COLS
        if not kwargs:
            kwargs = ATTRIBUTES

        columns = [v for v in kwargs.values()]
        if args:
            args = list(args)
            args.reverse()
            for i in range(0, len(args)):
                columns.insert(1, args[i])

            # 去重
            base_columns = list(set(columns))
            # 保持原有顺序
            base_columns.sort(key=columns.index)
        else:
            base_columns = columns

        # 设置属性名
        prefix = '__attribute_name'
        for item in self.attribute_list:
            kwargs[prefix + item] = item

        if isinstance(tables, str):
            if self.comma1 in tables:
                tables = tables.split(self.comma1)
            elif self.comma2 in tables:
                tables = tables.split(self.comma2)
            else:
                only_one_table = True
                metas = [self._get_table_meta(tables, base_columns)]

        if not only_one_table:
            if not isinstance(tables, set):
                tables = set(tables)
            metas = [self._get_table_meta(table.strip(), base_columns) for table in tables]

        no_key_tables = [meta for meta in metas if isinstance(meta, str)]
        if len(no_key_tables) > 0:
            print("There isn't primary key in the tables %s, it will not generate model class." % no_key_tables)

        metas = [meta for meta in metas if isinstance(meta, dict)]
        if len(metas) > 0:
            cols = [col for mata in metas for col in mata['super_columns']]
            col_dict = {col['COLUMN_NAME']: col for col in cols}

            def get_type(col):
                if col in col_dict:
                    return col_dict[col]['DATA_TYPE']
                elif col == kwargs.get(KEY) or col == kwargs.get(UPDATE_BY) or col == kwargs.get(DEL_FLAG):
                    return 'int'
                elif col == kwargs.get('__update_time__'):
                    return 'datetime'
                elif col.endswith("_time"):
                    return 'datetime'
                elif col.endswith("_date"):
                    return 'date'
                else:
                    return 'None'

            kwargs['metas'] = metas
            kwargs['base_columns'] = [{'COLUMN_NAME': col, 'DATA_TYPE': get_type(col)} for col in base_columns]
            self._generate(kwargs, path)

    def _get_table_meta(self, table: str, base_columns):
       raise NotImplementedError

    def _generate(self, metas: dict, path: str):
        loader = FileSystemLoader(searchpath=os.path.dirname(__file__))
        environment = Environment(loader=loader)
        tpl = environment.get_template(self.template)
        output = tpl.render(**metas)
        if path:
            suffix = '.py'
            path = path if path.endswith(suffix) else path + suffix
            with open(path, 'w', encoding='utf-8') as f:
                f.write(output)
            print('Model文件已生成：%s' % path)
        else:
            print(output)

    @staticmethod
    def _get_class_name(table):
        if '_' not in table:
            return table.capitalize()

        names = table.split('_')
        names = [name.capitalize() for name in names]
        return ''.join(names)