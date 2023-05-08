"""Populate

Revision ID: ba09343fb2cf
Revises: 3f4d76e9210d
Create Date: 2023-05-07 00:00:28.546504

"""

import logging
import psycopg2
from queries import sql_variant_lab2
from functions import fill_tables, create_result_file
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba09343fb2cf'
down_revision = '3f4d76e9210d'
branch_labels = None
depends_on = None


def upgrade():
    logging.info('Try connect to DataBase')
    connect = psycopg2.connect(dbname='zno', user='postgres', password='postgres', host='db')
    logging.info('Connect to DataBase sucсessful')

    with connect:
        cursor = connect.cursor()
        fill_tables(connect, cursor)
        create_result_file(cursor, 'Result_lab2')
        



def downgrade():
    pass
