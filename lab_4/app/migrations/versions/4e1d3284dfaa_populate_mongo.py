"""empty message

Revision ID: 4e1d3284dfaa
Revises: c6d219f055c1
Create Date: 2023-06-07 21:19:56.336248

"""
from alembic import op
import sqlalchemy as sa
import psycopg2
import time
from app import mongo_db



# revision identifiers, used by Alembic.
revision = '4e1d3284dfaa'
down_revision = 'c6d219f055c1'
branch_labels = None
depends_on = None


def upgrade():

    # Під'єднання до PostgreSQL
    pg_conn = psycopg2.connect(
        host="db",
        port=5432,
        database="zno",
        user="postgres",
        password="postgres"
    )
    pg_cursor = pg_conn.cursor()

    tries = 60
    while tries:
        try:
            # Отримання даних з таблиць PostgreSQL
            pg_cursor.execute("SELECT * FROM sex_type")
            rows = pg_cursor.fetchall()
            # Створення нової колекції в MongoDB та вставка даних
            mongo_collection_sex_type = mongo_db["sex_type"]
            for row in rows:
                document = {
                    "id": row[0],
                    "type": row[1],
                }

                mongo_collection_sex_type.insert_one(document)
            count = mongo_collection_sex_type.count_documents({})
            print(f'Записів у колекції sex_type {count}')
            # for el in mongo_collection_sex_type.find():
            #     print(el)


            # Отримання даних з таблиць PostgreSQL
            pg_cursor.execute("SELECT * FROM regname")
            rows = pg_cursor.fetchall()
            # Створення нової колекції в MongoDB та вставка даних
            mongo_collection_regname = mongo_db["regname"]
            for row in rows:
                document = {
                    "id": row[0],
                    "name": row[1],
                }
                
                mongo_collection_regname.insert_one(document)
            count = mongo_collection_regname.count_documents({})
            print(f'Записів у колекції regname {count}')


            # Отримання даних з таблиць PostgreSQL
            pg_cursor.execute("SELECT * FROM test_subj")
            rows = pg_cursor.fetchall()
            # Створення нової колекції в MongoDB та вставка даних
            mongo_collection_test_subj = mongo_db["test_subj"]
            for row in rows:
                document = {
                    "id": row[0],
                    "name": row[1],
                }
                
                mongo_collection_test_subj.insert_one(document)
            count = mongo_collection_test_subj.count_documents({})
            print(f'Записів у колекції test_subj {count}')


            # Отримання даних з таблиць PostgreSQL
            pg_cursor.execute("SELECT * FROM test_status")
            rows = pg_cursor.fetchall()
            # Створення нової колекції в MongoDB та вставка даних
            mongo_collection_test_status = mongo_db["test_status"]
            for row in rows:
                document = {
                    "id": row[0],
                    "status": row[1],
                }
                
                mongo_collection_test_status.insert_one(document)
            count = mongo_collection_test_status.count_documents({})
            print(f'Записів у колекції test_status {count}')


            # Отримання даних з таблиць PostgreSQL
            pg_cursor.execute("SELECT * FROM person")
            rows = pg_cursor.fetchall()
            # Створення нової колекції в MongoDB та вставка даних
            mongo_collection_person = mongo_db["person"]
            for row in rows:
                document = {
                    "outid": row[0],
                    "birth": row[1],
                    "sextype_id": row[2],
                    "regname_id": row[3],
                    "areaname": row[4],
                    "tername": row[5],
                    "regtypename": row[6],
                    "tertypename": row[7],
                    "classprofilename": row[8],
                    "classlangname": row[9],
                    "eoname": row[10],
                    "eotypename": row[11],
                    "eoregname": row[12],
                    "eoareaname": row[13],
                    "eotername": row[14],
                    "eoparent": row[15],
                }
                
                mongo_collection_person.insert_one(document)
            count = mongo_collection_person.count_documents({})
            print(f'Записів у колекції person {count}')


            # Отримання даних з таблиць PostgreSQL
            pg_cursor.execute("SELECT * FROM test")
            rows = pg_cursor.fetchall()
            # Створення нової колекції в MongoDB та вставка даних
            mongo_collection_test = mongo_db["test"]
            for row in rows:
                document = {
                    "id": row[0],
                    "outid": row[1],
                    "year": row[2],
                    "subject_id": row[3],
                    "status_id": row[4],
                    "ball100": row[5],
                    "ball12": row[6],
                    "ball": row[7],
                    "ptname": row[8],
                    "ptregname_id": row[9],
                    "ptareaname": row[10],
                    "pttername": row[11],
                }
                
                mongo_collection_test.insert_one(document)
            count = mongo_collection_test.count_documents({})
            print(f'Записів у колекції test {count}')



            # Закриття з'єднань
            pg_cursor.close()
            pg_conn.close()
            tries = 0
        
        except:
            print('Undefined error')
            tries -= 1
            time.sleep(2)



def downgrade():
    pass
