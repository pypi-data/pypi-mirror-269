import os
from sqlexec import Dialect, Engine
from sqlbatis import db, init_db
from typing import Union, Iterable
from jinja2 import FileSystemLoader, Environment
from sqlbatis.constant import KEY, TABLE, UPDATE_BY, UPDATE_TIME, DEL_FLAG, KEY_STRATEGY

COMMON_COLS = ['create_by', 'create_time']
ATTRIBUTES = {KEY: 'id', UPDATE_BY: 'update_by', UPDATE_TIME: 'update_time', DEL_FLAG: 'del_flag'}


class Generator:
    comma1 = ','
    comma2 = '，'
    sql = '''
    SELECT column_name, data_type, character_maximum_length, NUMERIC_precision, NUMERIC_scale, column_key FROM information_schema.columns
     WHERE table_schema = (SELECT DATABASE()) AND table_name = ? 
    '''

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
        Dialect.init(Engine.MYSQL)
        init_db(*args, **kwargs)

    def generate_with_schema(self, schema: str = None, path: str = None, *args, **kwargs):
        """
        coder = Generator(user='root', password='xxx', host='127.0.0.1', port=3306, database='testdb', driver='pymysql')
        coder.generate_with_schema('testdb', 'models.py')
        """

        if schema:
            db.execute('use %s' % schema)
        tables = db.select('show tables')
        tables = [table[0] for table in tables]
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
        for item in [KEY, TABLE, UPDATE_BY, UPDATE_TIME, DEL_FLAG, KEY_STRATEGY]:
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

    @staticmethod
    def _generate(metas: dict, path: str):
        loader = FileSystemLoader(searchpath=os.path.dirname(__file__))
        environment = Environment(loader=loader)
        tpl = environment.get_template('generator.tpl')
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