from sqlalchemy import create_engine
from sqlalchemy import inspect
from typing import TextIO, TypeVar, List
from datetime import datetime
import os
import time


DATE = os.getenv('DATE')
DATAPATH = os.getenv('DATAPATH')
DB_STRING = os.getenv('INITIAL_DB_STRING')


db = create_engine(DB_STRING)  # Starting connection with northwind db
inspector = inspect(db)  # Setting inspector to retrieve tables infos


def get_tables_data(table_names: List[str], paths: List[str]) -> str:
    with db.connect() as connection:
        try:
            cursor = connection.connection.cursor()
            for table_name, path in zip(table_names, paths):
                save_file = open(
                        f'{path}/{table_name}.csv', 'w', encoding='utf8')
                copy_query = f'COPY {table_name} TO STDOUT CSV HEADER'
                result = cursor.copy_expert(copy_query, save_file)
                connection.connection.commit()
                print(f'Content of {table_name} successfully saved!')
        except:
            raise


def get_table_names() -> List[str]:
    with db.connect() as connection:
        try:
            return inspector.get_table_names()
        except:
            pass


def create_directories(parent_path: str, table_names: List[str], date: str) \
        -> List[str]:  # Create new directory inside /data/csv
    directory_paths: List[str] = list()
    for table_name in table_names:
        try:
            full_path: str = os.path.join(parent_path, table_name, date)
            directory_paths.append(full_path)
            os.makedirs(full_path)
            print(f'Directory {full_path} successfully created!')
        except FileExistsError:
            pass

    return directory_paths


def check_date(date: str) -> str:  # Check for past date env variable
    if date == '' or date is None:
        date: str = str(datetime.today().date())
    else:
        try:
            date: str = str(datetime.strptime(date, '%Y-%m-%d').date())
        except ValueError as e:
            print('Incorrect date format change it to the iso format \
(YYYY-MM-DD) inside csv_worker/.csv_worker.env')
            raise e

    return date


if __name__ == "__main__":
    DATE: str = check_date(DATE)
    table_names: List[str] = get_table_names()
    save_paths: List[str] = create_directories(DATAPATH, table_names, DATE)
    get_tables_data(table_names, save_paths)
