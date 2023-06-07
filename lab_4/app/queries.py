"""Файл із деякими SQL запитами

"""


def sql_create_main_table():
    """Функція повертає строку, яка є SQL-запитом для створення бази даних, якщо такої не існує
       та primary key для колонки outid
    
    """
    query = '''
CREATE TABLE IF NOT EXISTS zno (
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
    CONSTRAINT zno_pk PRIMARY KEY (outid)
);
'''
    return query


def sql_create_progress_table():
    """Функція повертає строку, яка є SQL-запитом створення таблиці прогресу транзакцій

    """

    query = '''
CREATE TABLE IF NOT EXISTS progress (
    file varchar NOT NULL,
    status int4 NULL,
    parts int4 NULL,
    CONSTRAINT progress_pk PRIMARY KEY (file)
);    
'''
    return query


def sql_variant_lab2():
    """Функція повертає строку, яка є SQL-запитом за варіантом №6 для лаб 2

    """

    query = '''
SELECT regname.name, test.year, MIN(ball100) AS min_hist_score
FROM test
JOIN regname ON regname.id = test.ptregname_id
JOIN test_subj ON test_subj.id = test.subject_id
JOIN test_status ON test_status.id = test.status_id
WHERE test_subj.name = 'Історія України' AND test_status.status = 'Зараховано'
GROUP BY regname.name, test.year;
'''
    return query
