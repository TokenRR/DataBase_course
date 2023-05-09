'''
Лабораторна робота № 2
Тема: Docker,
      Flask-migrate,
      PostgreSQL,
      ERD-діаграми (Power Design)
      
Склад команди: Ромацький Микита, КМ-01
               Карачун Анастасія, КМ-02
               Шаповалов Гліб, КМ-03

Варіант: 6 - 'Порівняти найгірший бал з Історії України у кожному регіоні у 2020 та 2021 роках
              серед тих кому було зараховано тест'
'''


from queries import sql_create_main_table
from queries import sql_create_progress_table
from functions import populate


import time
import logging


import psycopg2


ZNO2020 = r'./data/OpenDataZNO2020'
ZNO2021 = r'./data/OpenDataZNO2021'


if __name__ == '__main__':
    """docker-compose build --no-cache && docker-compose up -d --force-recreate
    
    """

    logging.basicConfig(level=logging.INFO, format="[%(asctime)s | %(levelname)s ] %(message)s")
    
    tries = 30
    while tries:
        try:
            logging.info('Try connect to DataBase')
            connect = psycopg2.connect(dbname='zno', user='postgres', password='postgres', host='db')
            logging.info('Connect to DataBase sucсessful')

            with connect:
                cursor = connect.cursor()

                create_main_table = sql_create_main_table()
                cursor.execute(create_main_table)
                logging.info('Sucсessful create main table')

                create_progress_table = sql_create_progress_table()
                cursor.execute(create_progress_table)
                logging.info('Sucсessful create progress table')
                
                #-------------------------------------# 

                logging.info('Trying fill DataBase from files 2020`s year')
                populate(connect, cursor, 'windows-1251', ZNO2020, 2020)
                logging.info('Sucсessful fill DataBase from files 2020`s year')

                #-------------------------------------# 

                logging.info('Trying fill DataBase from files 2021`s year')
                populate(connect, cursor, 'utf-8-sig', ZNO2021, 2021)
                logging.info('Sucсessful fill DataBase from files 2021`s year')

                #-------------------------------------# 
                
                logging.info('Data is imported into the database in a single table `zno`')
                tries = 0

        except psycopg2.OperationalError as err:
            logging.warning(f'\nERROR: {err}\n')
            time.sleep(15)
        except psycopg2.errors.AdminShutdown as err:
            logging.warning(f'\nERROR: {err}\n')
        except psycopg2.InterfaceError as err:
            logging.warning(f'\nERROR: {err}\n')
        except FileNotFoundError as err:
            tries = 0
            logging.warning(f'\nERROR: {err}\n')
            logging.warning(f'\nFile {err.filename} does not exist\n')
