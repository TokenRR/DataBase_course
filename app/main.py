'''
Лабораторна робота № 1
Тема: Docker,
      Робота з РСКБД із Python коду,
      Побудова якісних data ingestion програм на основі Python,
Виконав: Ромацький Микита, КМ-01
Варіант: 6 - 'Порівняти найгірший бал з Історії України у кожному регіоні у 2020 та 2021 роках
              серед тих кому було зараховано тест'
'''


import csv
import time


import psycopg2


# ZNO2020 = r'..\data\Odata2020File.csv'
# ZNO2021 = r'..\data\Odata2021File.csv'
ZNO2020 = r'./Odata2020File.csv'
ZNO2021 = r'./Odata2021File.csv'


def mark(string):
    if string != 'null' and string is not None:
        return float(string.replace(',', '.'))
    
def insert(col, val):
    return f'INSERT INTO tbl_ZNO ({col}) VALUES ({val})'

# а цей конекшен треба буде і закривати чи 
create = '''
CREATE TABLE IF NOT EXISTS tbl_ZNO (
    OUTID uuid,
    Birth int NULL,
    SexTypeName varchar NULL,
    RegName varchar NULL,
    AREANAME varchar NULL,
    TERNAME varchar NULL,
    RegTypeName varchar NULL,
    TerTypeName varchar NULL,
    ClassProfileNAME varchar NULL,
    ClassLangName varchar NULL,
    EONAME varchar NULL,
    EOTypeName varchar NULL,
    EORegName varchar NULL,
    EOAreaName varchar NULL,
    EOTerName varchar NULL,
    EOParent varchar NULL,
    UMLTest varchar NULL,
    UMLTestStatus varchar NULL,
    UMLBall100 float NULL,
    UMLBall12 int NULL,
    UMLBall int NULL,
    UMLAdaptScale int NULL,
    UMLPTName varchar NULL,
    UMLPTRegName varchar NULL,
    UMLPTAreaName varchar NULL,
    UMLPTTerName varchar NULL,
    UkrTest varchar NULL,
    UkrSubTest varchar NULL,
    UkrTestStatus varchar NULL,
    UkrBall100 float NULL,
    UkrBall12 int NULL,
    UkrBall int NULL,
    UkrAdaptScale int NULL,
    UkrPTName varchar NULL,
    UkrPTRegName varchar NULL,
    UkrPTAreaName varchar NULL,
    UkrPTTerName varchar NULL,
    HistTest varchar NULL,
    HistLang varchar NULL,
    HistTestStatus varchar NULL,
    HistBall100 float NULL,
    HistBall12 int NULL,
    HistBall int NULL,
    HistPTName varchar NULL,
    HistPTRegName varchar NULL,
    HistPTAreaName varchar NULL,
    HistPTTerName varchar NULL,
    MathTest varchar NULL,
    MathLang varchar NULL,
    MathTestStatus varchar NULL,
    MathBall100 float NULL,
    MathBall12 int NULL,
    MathDpaLevel varchar NULL,
    MathBall int NULL,
    MathPTName varchar NULL,
    MathPTRegName varchar NULL,
    MathPTAreaName varchar NULL,
    MathPTTerName varchar NULL,
    MathStTest varchar NULL,
    MathStLang varchar NULL,
    MathStTestStatus varchar NULL,
    MathStBall12 int NULL,
    MathStBall int NULL,
    MathStPTName varchar NULL,
    MathStPTRegName varchar NULL,
    MathStPTAreaName varchar NULL,
    MathStPTTerName varchar NULL,
    PhysTest varchar NULL,
    PhysLang varchar NULL,
    PhysTestStatus varchar NULL,
    PhysBall100 float NULL,
    PhysBall12 int NULL,
    PhysBall int NULL,
    PhysPTName varchar NULL,
    PhysPTRegName varchar NULL,
    PhysPTAreaName varchar NULL,
    PhysPTTerName varchar NULL,
    ChemTest varchar NULL,
    ChemLang varchar NULL,
    ChemTestStatus varchar NULL,
    ChemBall100 float NULL,
    ChemBall12 int NULL,
    ChemBall int NULL,
    ChemPTName varchar NULL,
    ChemPTRegName varchar NULL,
    ChemPTAreaName varchar NULL,
    ChemPTTerName varchar NULL,
    BioTest varchar NULL,
    BioLang varchar NULL,
    BioTestStatus varchar NULL,
    BioBall100 float NULL,
    BioBall12 int NULL,
    BioBall int NULL,
    BioPTName varchar NULL,
    BioPTRegName varchar NULL,
    BioPTAreaName varchar NULL,
    BioPTTerName varchar NULL,
    GeoTest varchar NULL,
    GeoLang varchar NULL,
    GeoTestStatus varchar NULL,
    GeoBall100 float NULL,
    GeoBall12 int NULL,
    GeoBall int NULL,
    GeoPTName varchar NULL,
    GeoPTRegName varchar NULL,
    GeoPTAreaName varchar NULL,
    GeoPTTerName varchar NULL,
    EngTest varchar NULL,
    EngTestStatus varchar NULL,
    EngBall100 float NULL,
    EngBall12 int NULL,
    EngDPALevel varchar NULL,
    EngBall int NULL,
    EngPTName varchar NULL,
    EngPTRegName varchar NULL,
    EngPTAreaName varchar NULL,
    EngPTTerName varchar NULL,
    FraTest varchar NULL,
    FraTestStatus varchar NULL,
    FraBall100 float NULL,
    FraBall12 int NULL,
    FraDPALevel varchar NULL,
    FraBall varchar NULL,
    FraPTName varchar NULL,
    FraPTRegName varchar NULL,
    FraPTAreaName varchar NULL,
    FraPTTerName varchar NULL,
    DeuTest varchar NULL,
    DeuTestStatus varchar NULL,
    DeuBall100 float NULL,
    DeuBall12 int NULL,
    DeuDPALevel varchar NULL,
    DeuBall varchar NULL,
    DeuPTName varchar NULL,
    DeuPTRegName varchar NULL,
    DeuPTAreaName varchar NULL,
    DeuPTTerName varchar NULL,
    SpaTest varchar NULL,
    SpaTestStatus varchar NULL,
    SpaBall100 float NULL,
    SpaBall12 int NULL,
    SpaDPALevel varchar NULL,
    SpaBall varchar NULL,
    SpaPTName varchar NULL,
    SpaPTRegName varchar NULL,
    SpaPTAreaName varchar NULL,
    SpaPTTerName varchar NULL,
    YEAR int NULL,
    CONSTRAINT tbl_ZNO_pk PRIMARY KEY (outid)
);
'''

query = '''
SELECT RegName, YEAR, MIN(HistBall100) AS min_ball
FROM tbl_ZNO
WHERE HistTestStatus = 'Зараховано'
GROUP BY RegName, YEAR;
'''

tries = 999_999
while tries:
    try:
        conn = psycopg2.connect(dbname='znodata', user='postgres', password='postgres', host='db')

        print(f'\n[{time.strftime("%H:%M:%S", time.localtime())}] ! Connected !\n')

        with conn:
            start = time.time()  #  Старт таймера 
            cur = conn.cursor()
            cur.execute(create)
            print(f'\n[{time.strftime("%H:%M:%S", time.localtime())}] ! Table was created !\n')

            cur.execute('SELECT COUNT(outID) FROM tbl_ZNO WHERE year=2020')
            count_2020 = cur.fetchone()[0]
            print(f'\n[{time.strftime("%H:%M:%S", time.localtime())}] Entries in the table for 2020 before insert = {count_2020}\n')
                
            with open(ZNO2020, 'r', encoding='windows-1251') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                headers = next(reader)
                headers.append('YEAR')  #  Список назв колонок
                str_headers = ', '.join(headers)  #  Строка з усіх назв колонок -> 'OUTID, Birth, ...'
                idx_float = [headers.index(i) for i in headers if 'Ball100' in i]
                #  Індекси усіх колонок з типом флоат

                for row_id, row in enumerate(reader):
                    if row_id >= int(count_2020):
                        tmp_row = []
                        for el_id, el in enumerate(row):
                            if el_id in idx_float:
                                el = mark(el)
                                tmp_row.append(el)
                            else:
                                tmp_row.append(el)
                        lst_row = list(map(str, tmp_row))
                        lst_row.append('2020')
                        lst_row = [x.replace("\'", "`") for x in lst_row]
                        tmp_str = ''
                        for i in lst_row:
                            tmp_str += "\'" + i + "\', "
                        str_row = tmp_str[:-2]
                        str_row = str_row.replace("\'null\'", "null")
                        str_row = str_row.replace("\'None\'", "null")
                        str_insert = insert(str_headers, str_row)
                        cur.execute(str_insert) 
                        if row_id % 1000 == 0:
                            conn.commit()
                conn.commit()
            cur.execute('SELECT COUNT(outID) FROM tbl_ZNO WHERE year=2020')
            count_2020 = cur.fetchone()[0]
            print(f'\n[{time.strftime("%H:%M:%S", time.localtime())}] Entries in the table for 2020 after insert {count_2020}\n')


            cur.execute('SELECT COUNT(outID) FROM tbl_ZNO WHERE year=2021')
            count_2021 = cur.fetchone()[0]
            print(f'\n[{time.strftime("%H:%M:%S", time.localtime())}] Entries in the table for 2021 before insert = {count_2021}\n')
	    
            with open(ZNO2021, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                headers = next(reader)
                headers.append('YEAR')  #  Список назв колонок
                str_headers = ', '.join(headers)  #  Строка з усіх назв колонок -> 'OUTID, Birth, ...'
                idx_float = [headers.index(i) for i in headers if 'Ball100' in i]
                #  Індекси усіх колонок з типом флоат

                for row_id, row in enumerate(reader):
                    if row_id >= int(count_2021):
                        tmp_row = []
                        for el_id, el in enumerate(row):
                            if el_id in idx_float:
                                el = mark(el)
                                tmp_row.append(el)
                            else:
                                tmp_row.append(el)
                        lst_row = list(map(str, tmp_row))
                        lst_row.append('2021')
                        lst_row = [x.replace("\'", "`") for x in lst_row]
                        tmp_str = ''
                        for i in lst_row:
                            tmp_str += "\'" + i + "\', "
                        str_row = tmp_str[:-2]
                        str_row = str_row.replace("\'null\'", "null")
                        str_row = str_row.replace("\'None\'", "null")
                        str_insert = insert(str_headers, str_row)
                        cur.execute(str_insert) 
                        if row_id % 1000 == 0:
                            conn.commit()
                conn.commit()
            cur.execute('SELECT COUNT(outID) FROM tbl_ZNO WHERE year=2021')
            count_2021 = cur.fetchone()[0]
            print(f'\n[{time.strftime("%H:%M:%S", time.localtime())}] Entries in the table for 2021 after insert {count_2021}\n')

            cur.execute('SELECT COUNT(outID) FROM tbl_ZNO')
            count_all = cur.fetchone()[0]
            print(f'\n[{time.strftime("%H:%M:%S", time.localtime())}] Entries in the table for all years after insert {count_all}\n')
            # Select * ^

            print(f'\n[{time.strftime("%H:%M:%S", time.localtime())}] ! All data successfuly inserted !\n')


        with open(r'execution_time.txt', 'w') as timefile:
            timefile.write(f'Execution time: {round(time.time() - start, 2)} s')
        print(f'\n[{time.strftime("%H:%M:%S", time.localtime())}] Execution time: {round(time.time() - start, 2)} s\n')


        cur.execute(query)
        # try:
        #     query_result = cur.fetchall()
        #     for row in query_result:
        #         print(row)
        # except:
        #     pass
        with open(r'ZNOdata.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([col[0] for col in cur.description])

            for row in cur:
                writer.writerow([str(el) for el in row])
        print(f'\n[{time.strftime("%H:%M:%S", time.localtime())}] ! Created file ZNOdata.csv with statistics !\n')
        
        
        tries = 0
    
    except psycopg2.OperationalError as err:
        print('\nOperationalError')
        print(err)
        time.sleep(10)
    
    except FileNotFoundError as err:
        tries = 0
        print('\nFileNotFoundError')
        print(f'File {err.filename} does not exist')

    except psycopg2.errors.AdminShutdown as err:
        print(err)

    except psycopg2.InterfaceError as err:
        print(err)