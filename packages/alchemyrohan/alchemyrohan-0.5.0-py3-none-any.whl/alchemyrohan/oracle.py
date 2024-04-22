

__all__ = ['read_oracle_and_build_code']


from typing import Any
from datetime import datetime
from datetime import timedelta
from sqlalchemy.dialects.oracle import BINARY_DOUBLE
from sqlalchemy.dialects.oracle import BINARY_FLOAT
from sqlalchemy.dialects.oracle import BLOB
from sqlalchemy.dialects.oracle import CHAR
from sqlalchemy.dialects.oracle import CLOB
from sqlalchemy.dialects.oracle import DATE
from sqlalchemy.dialects.oracle import DOUBLE_PRECISION
from sqlalchemy.dialects.oracle import FLOAT
from sqlalchemy.dialects.oracle import INTERVAL
from sqlalchemy.dialects.oracle import LONG
from sqlalchemy.dialects.oracle import NCHAR
from sqlalchemy.dialects.oracle import NCLOB
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.dialects.oracle import NVARCHAR
from sqlalchemy.dialects.oracle import NVARCHAR2
from sqlalchemy.dialects.oracle import RAW
from sqlalchemy.dialects.oracle import REAL
from sqlalchemy.dialects.oracle import ROWID
from sqlalchemy.dialects.oracle import TIMESTAMP
from sqlalchemy.dialects.oracle import VARCHAR
from sqlalchemy.dialects.oracle import VARCHAR2

from alchemyrohan.meta_data import MetaDataHolder
from alchemyrohan.utils import str_print


dialect_imports = []


def get_default(typ: str) -> Any:
    if typ == 'BINARY_DOUBLE':
        return 0.0
    if typ == 'BINARY_FLOAT':
        return 0.0
    if typ == 'BLOB':
        return b"' '"
    if typ == 'CHAR':
        return "' '"
    if typ == 'CLOB':
        return "' '"
    if typ == 'DATE':
        return datetime.today()
    if typ == 'DOUBLE_PRECISION':
        return 0.0
    if typ == 'FLOAT':
        return 0.0
    if typ == 'INTERVAL':
        return timedelta(days=1, hours=1, minutes=1)
    if typ == 'LONG':
        return "' '"
    if typ == 'NCHAR':
        return "' '"
    if typ == 'NCLOB':
        return "' '"
    if typ == 'NUMBER':
        return 0
    if typ == 'NVARCHAR':
        return "' '"
    if typ == 'NVARCHAR2':
        return "' '"
    if typ == 'RAW':
        return b"' '"
    if typ == 'REAL':
        return 0.0
    if typ == 'ROWID':
        return "' '"
    if typ == 'TIMESTAMP':
        return datetime.now()
    if typ == 'VARCHAR':
        return "' '"
    if typ == 'VARCHAR2':
        return "' '"


def get_type_name(typ: Any) -> str:
    if isinstance(typ, BINARY_DOUBLE):
        return 'BINARY_DOUBLE'
    if isinstance(typ, BINARY_FLOAT):
        return 'BINARY_FLOAT'
    if isinstance(typ, BLOB):
        return 'BLOB'
    if isinstance(typ, CHAR):
        return 'CHAR'
    if isinstance(typ, CLOB):
        return 'CLOB'
    if isinstance(typ, DATE):
        return 'DATE'
    if isinstance(typ, DOUBLE_PRECISION):
        return 'DOUBLE_PRECISION'
    if isinstance(typ, FLOAT):
        return 'FLOAT'
    if isinstance(typ, INTERVAL):
        return 'INTERVAL'
    if isinstance(typ, LONG):
        return 'LONG'
    if isinstance(typ, NCHAR):
        return 'NCHAR'
    if isinstance(typ, NCLOB):
        return 'NCLOB'
    if isinstance(typ, NUMBER):
        return 'NUMBER'
    if isinstance(typ, NVARCHAR):
        return 'NVARCHAR'
    if isinstance(typ, NVARCHAR2):
        return 'NVARCHAR2'
    if isinstance(typ, RAW):
        return 'RAW'
    if isinstance(typ, REAL):
        return 'REAL'
    if isinstance(typ, ROWID):
        return 'ROWID'
    if isinstance(typ, TIMESTAMP):
        return 'TIMESTAMP'
    if isinstance(typ, VARCHAR):
        return 'VARCHAR'
    if isinstance(typ, VARCHAR2):
        return 'VARCHAR2'


def get_type_prop(typ: Any) -> str:
    if isinstance(typ, BINARY_DOUBLE):
        return 'BINARY_DOUBLE'
    if isinstance(typ, BINARY_FLOAT):
        return 'BINARY_FLOAT'
    if isinstance(typ, BLOB):
        return 'BLOB'
    if isinstance(typ, CHAR):
        return f'CHAR({typ.length})'
    if isinstance(typ, CLOB):
        return f'CLOB({typ.length})'
    if isinstance(typ, DATE):
        return 'DATE'
    if isinstance(typ, DOUBLE_PRECISION):
        return 'DOUBLE_PRECISION'
    if isinstance(typ, FLOAT):
        return f'FLOAT({typ.precision},{typ.scale})'
    if isinstance(typ, INTERVAL):
        return 'INTERVAL'
    if isinstance(typ, LONG):
        return f'LONG({typ.length})'
    if isinstance(typ, NCHAR):
        return f'NCHAR({typ.length})'
    if isinstance(typ, NCLOB):
        return f'NCLOB({typ.length})'
    if isinstance(typ, NUMBER):
        return f'NUMBER({typ.precision},{typ.scale})'
    if isinstance(typ, NVARCHAR):
        return f'NVARCHAR({typ.length})'
    if isinstance(typ, NVARCHAR2):
        return f'NVARCHAR2({typ.length})'
    if isinstance(typ, RAW):
        return 'RAW'
    if isinstance(typ, REAL):
        return f'REAL({typ.precision},{typ.scale})'
    if isinstance(typ, ROWID):
        return 'ROWID'
    if isinstance(typ, TIMESTAMP):
        return 'TIMESTAMP'
    if isinstance(typ, VARCHAR):
        return f'VARCHAR({typ.length})'
    if isinstance(typ, VARCHAR2):
        return f'VARCHAR2({typ.length})'


def columns(code_holder: dict, table_meta_data: MetaDataHolder) -> None:
    
    col = []
    for c in table_meta_data.columns:
        
        tmp = f"{c['name']} = Column("
        tmp = ''.join([tmp, get_type_prop(c['type'])])

        imp = f"from sqlalchemy.dialects.oracle import"\
            f" {get_type_name(c['type'])}"
        if imp not in dialect_imports:
            dialect_imports.append(imp)

        pk = False
        for k, v in table_meta_data.primary_key.items():
            if k == 'constrained_columns':
                for e in v:
                    if c['name'] == e:
                        tmp = ', '.join([tmp, 'primary_key=True'])
                        pk = True
                        break
                break

        if not pk:
            for f in table_meta_data.foreign_keys:
                for fk in f['referred_columns']:
                    if fk == c['name']:
                        ref_table = f['referred_table']
                        tmp = ', '.join(
                            [tmp, f"ForeignKey('{ref_table}.{fk}')"])
                        imp = 'from sqlalchemy import ForeignKey'
                        if imp not in dialect_imports:
                            dialect_imports.append(imp)
                        break

            if c['nullable']:
                tmp = ', '.join([tmp, 'nullable=True', 'default=None'])
            else:
                if c['default']:
                    tmp = ', '.join([
                        tmp, 'nullable=False', f"default={c['default']}"]
                        )
                else:
                    tmp = ', '.join([
                        tmp, 
                        'nullable=False', 
                        f"default={get_default(get_type_name(c['type']))}"
                        ]
                        )         

            for u in table_meta_data.unique_keys:
                for e in u['column_names']:
                    if c['name'] == e:
                        tmp = ', '.join([tmp, 'unique=True'])
                        break

        tmp = ''.join([tmp, ')'])

        tmp = f"""
    {tmp}"""
        
        col.append(tmp)
       
    code_holder.update({'columns': col})


def relations(code_holder: dict, table_meta_data: MetaDataHolder) -> None:

    rel = []
    for f in table_meta_data.foreign_keys:
        referred_table = f['referred_table']
        tmp = (f'parent_{referred_table.capitalize()}'
               f' = relationship("{referred_table.capitalize()}", '
               f'back_populates='
               f'"children_{table_meta_data.name.capitalize()}", '
               f'lazy="joined")')
        tmp = f"""
    {tmp}""" 
        rel.append(tmp)

    for k, v in table_meta_data.multi_foreign_keys.items():
        if k[1] == table_meta_data.name and not v:
            for child_table, r in table_meta_data.multi_foreign_keys.items():
                if r:
                    for rt in r:
                        if rt['referred_table'] == table_meta_data.name:
                            tmp = (f'children_{child_table[1].capitalize()}'
                                   f' = relationship('
                                   f'"{child_table[1].capitalize()}", '
                                   f'back_populates='
                                   f'"parent_{table_meta_data.name.capitalize()}", '
                                   f'lazy="joined")')
                            tmp = f"""
    {tmp}"""
                            rel.append(tmp)
            break
    if rel:
        imp = 'from sqlalchemy.orm import relationship'
        if imp not in dialect_imports:
            dialect_imports.append(imp)
    code_holder.update(
        {'imports': code_holder['imports'] + dialect_imports}
        )
    code_holder.update({'relations': rel})


def read_oracle_and_build_code(
        code_holder: dict, table_meta_data: MetaDataHolder) -> None:

    columns(code_holder, table_meta_data)
    relations(code_holder, table_meta_data)
    str_print(code_holder, table_meta_data)
