

__all__ = ['assemble_models']

import os
import argparse

from typing import Iterable
from sqlalchemy import create_engine
from sqlalchemy import Engine

from alchemyrohan.meta_data import MetaDataHolder
from alchemyrohan.wizard import generate_code
from alchemyrohan.wizard import construct_model
from alchemyrohan.wizard import generate_model
from alchemyrohan.wizard import generate_init_file


def assemble_models(
        conn_str: str,
        table_names: Iterable[str],
        path: str = '',
        py_path: str = 'py_path_to_model') -> None:
    """Creates database models for SqlAlchemy.

    Args:
        conn_str (str): Connection string to connect to the database.
        table_names (List[str]): Names of the tables from database.
        path (str, optional): Absolute path to the location where the
                              created models will be saved. Defaults
                              to the current directory.
        py_path (str, optional): Pythonic path to the models in the project.
                                 For example, 'project_name.db.models'.
                                 This will be written in code as:
                    'from project_name.db.models.TableName import TableName'.
    Raises:
        SQLAlchemyError: if connection or other issues appear.
    """

    if not path:
        path = os.getcwd()
    
    engine: Engine = create_engine(conn_str)
    for table in table_names:
        code_holder = generate_code(MetaDataHolder(engine, table), py_path)

        model_template = construct_model(code_holder)

        generate_model(table, model_template, path)

        generate_init_file(table, path, py_path)


def main() -> None:
    """
    Read arguments from the command line
    and call the function 'assemble_models()'.

    usage: arohan [-h] -c CONN_STR [-p PATH] [-y PY_PATH] -m MODELS

    options:
      -h, --help            show help message and exit
      -c CONN_STR, --conn_str CONN_STR
                            Connection string to connect with the
                            database - Required argument. Accepts a string.
      -p PATH, --path PATH  Path where to save the models - Optional argument.
                            Defaults to the current working directory.
                            Accepts a string.
      -y PY_PATH, --py_path PY_PATH
                            Pythonic path to models in the project.
                            Optional argument. Defaults to 'py_path'.
                            Accepts a string.
      -m MODELS, --models MODELS
                        Names of the database tables.
                        Required argument. Add every table with -m=
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--conn_str',
        type=str,
        help='Connection string to connect with the database'
             ' - Required argument. Accepts a string.',
        required=True)
    parser.add_argument(
        '-p', '--path',
        type=str,
        help='Path where to save the models - '
             'Optional argument. Defaults to the current '
             'working directory. Accepts a string.',
        default=os.getcwd())
    parser.add_argument(
        '-y', '--py_path',
        type=str,
        help="Pythonic path to models in the project. "
             "Optional argument. Defaults to 'py_path'. "
             "Accepts a string.",
        default='py_path')
    parser.add_argument(
        '-m', '--models',
        help='Names of the database tables. '
             'Required argument. Add every table with -m=',
        action='append',
        default=[],
        required=True)

    args = parser.parse_args()

    assemble_models(args.conn_str, args.models, args.path, args.py_path)


if __name__ == '__main__':
    main()
    