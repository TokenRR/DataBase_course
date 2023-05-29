"""Файл для створення фінального запиту по варіанту"""

from functions import create_result_file_lab2
import logging
import psycopg2

logging.info('Try connect to DataBase')
connect = psycopg2.connect(dbname='zno', user='postgres', password='postgres', host='db')
logging.info('Connect to DataBase sucсessful')

with connect:
    cursor = connect.cursor()
    create_result_file_lab2(cursor, 'Result_lab2')