from sqlalchemy import create_engine
from sqlalchemy import inspect
from typing import TextIO, TypeVar, List
from datetime import datetime
import os
import sys
import time
import glob


DATE = os.getenv('DATE')
DATAPATH = os.getenv('DATAPATH')
DB_STRING = os.getenv('FINAL_DB_STRING')


db = create_engine(DB_STRING)  # Starting connection with northwind db
inspector = inspect(db)  # Setting inspector to retrieve tables infos


def extract_data() -> None:
    with db.connect() as connection:
        cursor = connection.connection.cursor()
        f: TextIO = open('/extracted_data/orders_with_details.csv', 'w', encoding='utf8')
        extract_query: str = 'SELECT * FROM orders as o, order_details as od WHERE o.order_id = od.order_id'
        print('Extracting data to file')
        copy_query = f'COPY ({extract_query}) TO STDOUT CSV HEADER'
        result = cursor.copy_expert(copy_query, f)
        connection.connection.commit()
        print('Data successfully extracted!')


def delete_data() -> None:
    with db.connect() as connection:
        cursor = connection.connection.cursor()
        f: TextIO = open('./delete_data.sql', 'r', encoding='utf8')
        print('Cleaning data...')
        cursor.execute(f.read())
        connection.connection.commit()
        print('Data successfully cleaned!')


def drop_constraints() -> None:
    with db.connect() as connection:
        cursor = connection.connection.cursor()
        f: TextIO = open('./drop_constraints.sql')
        print('Dropping constraints...')
        cursor.execute(f.read())
        connection.connection.commit()
        print('Constraints successfully dropped!')


def add_constraints() -> None:
    with db.connect() as connection:
        cursor = connection.connection.cursor()
        f: TextIO = open('./add_constraints.sql')
        print('Adding constraints...')
        cursor.execute(f.read())
        connection.connection.commit()
        print('Constraints successfully added!')


def set_tables_data(paths: List[str], table_names: List[str]) -> str:
    paths.sort()
    table_names.sort()
    with db.connect() as connection:
        try:
            cursor = connection.connection.cursor()
            for table_name, path in zip(table_names, paths):
                saved_file = open(path, 'r', encoding='utf8')
                copy_query = f"COPY {table_name} FROM STDIN CSV HEADER DELIMITER ','"
                print(f'Copying data from {path} to table {table_name}...')
                result = cursor.copy_expert(copy_query, saved_file)
                connection.connection.commit()
        except:
            raise
    print('Data successfully copied!')


def get_file_paths(path: str, date: str) -> List[str]:
    files = glob.glob(f'{path}/*/{date}/*', recursive=True)
    if files:
        return files
    else:
        print('Files not found. Have you runned the first step?')
        sys.exit(1)


def check_files(files: List[str], tables: List[str]) -> bool:
    tables.sort()
    files.sort()
    if len(files) == len(tables):
            return True
    else:
        splitted_files: List[str] = list()
        for file_ in files:
            splitted_files.append(file_.split('/')[-1].rstrip('csv').rstrip('.'))
        missing_files:List[str] = list(set(tables) - set(splitted_files))
        print(f'There are missing .csv files in the /data directory. Please make sure that you have executed successfully the first part of the pipeline.\nMissing files:\n  {missing_files}')
        return False


def get_table_names() -> List[str]:
    with db.connect() as connection:
        try:
            return inspector.get_table_names()
        except:
            pass


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
    paths: List[str] = get_file_paths(DATAPATH, DATE)
    if check_files(paths, table_names):
        
        print('funcionou')
    else:
        print('Nao rolou')
    drop_constraints()
    delete_data()
    set_tables_data(paths, table_names)
    add_constraints()
    extract_data()
