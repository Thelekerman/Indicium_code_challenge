from typing import TextIO
from datetime import datetime
import os
import time


DATE = os.getenv('DATE')
DATAPATH = os.getenv('DATAPATH')


def get_data() -> str:  # Load data from CSV file
    f: TextIO = open('./order_details.csv', 'r', encoding='utf8')
    data = f.read()
    f.close()

    return data


def create_directory(parent_path: str, directory_name: str) -> str:  \
        # Create new directory inside /data/csv
    full_path: str = os.path.join(parent_path, directory_name)
    try:
        os.mkdir(full_path)
        print('Directory seccessfully created!')
    except FileExistsError:
        pass

    return full_path


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


def save_data(data: str, path: str) -> None:
    print('Saving data to file...')
    f: TextIO = open(f'{path}/order_details.csv', 'w')
    f.write(data)
    print('Data saved to file...')
    f.close()


if __name__ == "__main__":
    DATE: str = check_date(DATE)
    save_path: str = create_directory(DATAPATH, DATE)
    csv_data: str = get_data()
    save_data(csv_data, save_path)
