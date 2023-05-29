"""Файл із деякими основними функціями

"""


import queries


import logging
import csv
import os
import itertools


import psycopg2


def init_status(connect, folder_with_parts):
    """Функція перевірки прогресу внесення даних у базу
    
    """

    with connect.cursor() as cursor:
        cursor.execute('SELECT file,status,parts FROM progress WHERE file = %s',(folder_with_parts,))
        res = cursor.fetchone()
        if res is None:
            print(f'Creating new status tracker for {folder_with_parts}')      
            init_status = 0
            row_count = len(os.listdir(folder_with_parts))
            cursor.execute('''INSERT INTO progress (file, status, parts)
                              VALUES (%s, %s, %s)''', (folder_with_parts, init_status, row_count))
            print(f'Finished creating new status tracker for file {folder_with_parts}')
        return res if res else (folder_with_parts,init_status,row_count)


def fill_table(connect, cursor, file, encoding, year, i):
    """Функція внесення даних у базу та зміни прогресу у відповідній таблиці

    """

    if year == 2021:
        str_headers = """outid,birth,sextypename,regname,areaname,tername,regtypename,tertypename,classprofilename,classlangname,eoname,eotypename,eoregname,eoareaname,eotername,eoparent,
umltest,umlteststatus,umlball100,umlball12,umlball,umladaptscale,umlptname,umlptregname,umlptareaname,umlpttername,
ukrtest,ukrsubtest,ukrteststatus,ukrball100,ukrball12,ukrball,ukradaptscale,ukrptname,ukrptregname,ukrptareaname,ukrpttername,
histtest,histlang,histteststatus,histball100,histball12,histball,histptname,histptregname,histptareaname,histpttername,
mathtest,mathlang,mathteststatus,mathball100,mathball12,mathdpalevel,mathball,mathptname,mathptregname,mathptareaname,mathpttername,mathsttest,mathstlang,mathstteststatus,mathstball12,mathstball,mathstptname,mathstptregname,mathstptareaname,mathstpttername,
phystest,physlang,physteststatus,physball100,physball12,physball,physptname,physptregname,physptareaname,physpttername,
chemtest,chemlang,chemteststatus,chemball100,chemball12,chemball,chemptname,chemptregname,chemptareaname,chempttername,
biotest,biolang,bioteststatus,bioball100,bioball12,bioball,bioptname,bioptregname,bioptareaname,biopttername,
geotest,geolang,geoteststatus,geoball100,geoball12,geoball,geoptname,geoptregname,geoptareaname,geopttername,
engtest,engteststatus,engball100,engball12,engdpalevel,engball,engptname,engptregname,engptareaname,engpttername,
fratest,frateststatus,fraball100,fraball12,fradpalevel,fraball,fraptname,fraptregname,fraptareaname,frapttername,
deutest,deuteststatus,deuball100,deuball12,deudpalevel,deuball,deuptname,deuptregname,deuptareaname,deupttername,
spatest,spateststatus,spaball100,spaball12,spadpalevel,spaball,spaptname,spaptregname,spaptareaname,spapttername"""
    elif year == 2020:
        str_headers = '''outid,birth,sextypename,regname,areaname,tername,regtypename,tertypename,classprofilename,classlangname,eoname,eotypename,eoregname,eoareaname,eotername,eoparent,
ukrtest,ukrteststatus,ukrball100,ukrball12,ukrball,ukradaptscale,ukrptname,ukrptregname,ukrptareaname,ukrpttername,
histtest,histlang,histteststatus,histball100,histball12,histball,histptname,histptregname,histptareaname,histpttername,
mathtest,mathlang,mathteststatus,mathball100,mathball12,mathball,mathptname,mathptregname,mathptareaname,mathpttername,
phystest,physlang,physteststatus,physball100,physball12,physball,physptname,physptregname,physptareaname,physpttername,
chemtest,chemlang,chemteststatus,chemball100,chemball12,chemball,chemptname,chemptregname,chemptareaname,chempttername,
biotest,biolang,bioteststatus,bioball100,bioball12,bioball,bioptname,bioptregname,bioptareaname,biopttername,
geotest,geolang,geoteststatus,geoball100,geoball12,geoball,geoptname,geoptregname,geoptareaname,geopttername,
engtest,engteststatus,engball100,engball12,engdpalevel,engball,engptname,engptregname,engptareaname,engpttername,
fratest,frateststatus,fraball100,fraball12,fradpalevel,fraball,fraptname,fraptregname,fraptareaname,frapttername,
deutest,deuteststatus,deuball100,deuball12,deudpalevel,deuball,deuptname,deuptregname,deuptareaname,deupttername,
spatest,spateststatus,spaball100,spaball12,spadpalevel,spaball,spaptname,spaptregname,spaptareaname,spapttername'''
    else:
        return 'Wrong year'
    try:
        with open(file, encoding=encoding, mode='r') as f:
            dirr = os.path.dirname(file)
            cursor.execute(f'CREATE TEMP TABLE tmp_table ON COMMIT DROP AS TABLE zno WITH NO DATA')
            cursor.execute(f'ALTER TABLE tmp_table ALTER COLUMN year SET DEFAULT {year}')
            cursor.copy_expert(f"COPY tmp_table({str_headers}) FROM STDIN (DELIMITER ';', FORMAT CSV, HEADER true, NULL 'null')", f)
            cursor.execute(f'''INSERT INTO zno ({str_headers},year)
                               SELECT {str_headers},year FROM tmp_table''')
            cursor.execute("UPDATE public.progress SET status = %s WHERE file = %s", (i+1,dirr))
            connect.commit()
    except psycopg2.OperationalError as err:
        logging.warning(f'Failed to upload {file} with exception {err}')
        fill_table(connect, file, encoding, year, i)


def populate(connect, cursor, encoding, folder_with_parts, year):
    """Внесення даних у базу, якщо такої транзакції ще не було

    """

    folder = os.path.abspath(folder_with_parts)
    ls = os.listdir(folder); ls.sort()

    _,status,parts = init_status(connect, folder)
    for i, file in zip(range(status, parts), itertools.islice(ls, status, parts)):
        file = os.path.join(folder, file)
        fill_table(connect, cursor, file, encoding, year, i)
        _,status,parts = init_status(connect, folder)
        print(f'Uploaded [{status}/{parts}]: {folder_with_parts}')


def create_result_file_lab2(cursor, name):
    """Функція створення csv файлу із результатом запиту по варіанту

    """

    with open(f'{name}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        query = queries.sql_variant_lab2()
        cursor.execute(query)
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([col[0] for col in cursor.description])

        for row in cursor:
            writer.writerow([str(el) for el in row])


def fill_tables(connect, cursor):
    """Функція переносу даних із великої таблиці zno в таблиці після міграції

    """
    
    LIM = 999_000  # Константа для заповнення таблиці person. Визначає скільки людей за 1 рік ми берем.
    # Загальна сума записів буде вдвічі більша за цю константу

    print('Try fill sex_type table')
    sex_type = ['чоловіча', 'жіноча']
    for el in sex_type:
        cursor.execute(f"""INSERT INTO sex_type (type) VALUES ('{el}');""")
    connect.commit()
    print('Sucсessful fill sex_type table')


    print('Try fill regname table')
    regname = ['Дніпропетровська область', 'Кіровоградська область', 'Івано-Франківська область', 
        'Київська область', 'Одеська область', 'м.Київ', 'Чернігівська область', 'Львівська область',
        'Волинська область', 'Луганська область', 'Харківська область', 'Чернівецька область', 
        'Сумська область', 'Запорізька область', 'Херсонська область', 'Закарпатська область',
        'Хмельницька область', 'Тернопільська область', 'Черкаська область', 'Донецька область',
        'Рівненська область', 'Миколаївська область', 'Полтавська область',
        'Житомирська область', 'Вінницька область']
    for el in regname:
        cursor.execute(f"""INSERT INTO regname (name) VALUES ('{el}');""")
    connect.commit()
    print('Sucсessful fill regname table')


    print('Try fill test_status table')
    test_status = ['Зараховано', 'Не з’явився', 'Не подолав поріг', 'Не обрано 100-200', 'Анульовано']
    for el in test_status:
        cursor.execute(f"""INSERT INTO test_status (status) VALUES ('{el}');""")
    connect.commit()
    print('Sucсessful fill test_status table')


    print('Try fill test_subj table')
    test_subj = ['Українська мова та література', 'Українська мова', 'Історія України', 'Математика',
        'Фізика', 'Хімія', 'Біологія', 'Географія', 'Англійська мова',
        'Французька мова', 'Німецька мова', 'Іспанська мова']
    for el in test_subj:
        cursor.execute(f"""INSERT INTO test_subj (name) VALUES ('{el}');""")
    connect.commit()
    print('Sucсessful fill test_subj table')


    print('Try fill person table where year = 2020')
    cursor.execute(f"""INSERT INTO person (outid, birth, sextype_id, regname_id, areaname, tername,
        regtypename, tertypename, classprofilename, classlangname, eoname, eotypename, eoregname, eoareaname,
        eotername, eoparent)
        SELECT zno.OUTID, zno.Birth, sex_type.id, regname.id, zno.AREANAME, zno.TERNAME, zno.RegTypeName,
        zno.TerTypeName, zno.ClassProfileNAME, zno.ClassLangName, zno.EONAME, zno.EOTypeName, zno.EORegName,
        zno.EOAreaName, zno.EOTerName, zno.EOParent
        FROM zno
        JOIN sex_type ON zno.SexTypeName = sex_type.type
        JOIN regname ON zno.RegName = regname.name
        WHERE zno.year=2020
        LIMIT {LIM};""")
    connect.commit()
    print('Sucсessful fill person table where year = 2020')

    print('Try fill person table where year = 2021')
    cursor.execute(f"""INSERT INTO person (outid, birth, sextype_id, regname_id, areaname, tername,
        regtypename, tertypename, classprofilename, classlangname, eoname, eotypename, eoregname, eoareaname,
        eotername, eoparent)
        SELECT zno.OUTID, zno.Birth, sex_type.id, regname.id, zno.AREANAME, zno.TERNAME, zno.RegTypeName,
        zno.TerTypeName, zno.ClassProfileNAME, zno.ClassLangName, zno.EONAME, zno.EOTypeName, zno.EORegName,
        zno.EOAreaName, zno.EOTerName, zno.EOParent
        FROM zno
        JOIN sex_type ON zno.SexTypeName = sex_type.type
        JOIN regname ON zno.RegName = regname.name
        WHERE zno.year=2021
        LIMIT {LIM};""")
    connect.commit()
    print('Sucсessful fill person table where year = 2021')
    

    print('Try fill test table')
    subjects = ['UML', 'Ukr', 'Hist', 'Math', 'Phys', 'Chem', 'Bio', 'Geo', 'Eng', 'Fra', 'Deu', 'Spa']
    for s in subjects:
        print(f'Try fill for {s} subject')
        cursor.execute(f"""INSERT INTO test (outid, year, subject_id, status_id, ball100, ball12, ball, 
            ptname, ptregname_id, ptareaname, pttername)
            SELECT person.outid, zno.YEAR, test_subj.id, test_status.id, zno.{s}ball100, zno.{s}ball12,
            zno.{s}ball, zno.{s}PTName, regname.id, zno.{s}PTAreaName, zno.{s}PTTerName 
            FROM zno
            JOIN person ON zno.outid = person.outid
            JOIN regname ON zno.RegName = regname.name
            JOIN test_status ON zno.{s}TestStatus = test_status.status
            JOIN test_subj ON zno.{s}Test = test_subj.name;""")
        print(f'Sucсessful fill for {s} subject')
        connect.commit()
    print('Sucсessful fill test table')
