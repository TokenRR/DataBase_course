import pickle
from sqlalchemy.sql import func
from app import db, r
from app.models import Test, TestStatus, TestSubj, Regname
from . import person as person_service
from app import NAME_DATA_BASE, mongo_db


def serialize_test_all(person_uuid):
    if NAME_DATA_BASE in ['postgres']:
        tests = db.session.execute(db.select(Test).filter(Test.outid == person_uuid)).scalars()
    else:
        tests = mongo_db.test.find({"outid": person_uuid})
    return tests

def serialize_test(id):
    if NAME_DATA_BASE in ['postgres']:
        test = db.one_or_404(db.select(Test).filter(Test.id == id))
    else:
        test = mongo_db.test.find_one({"_id": id})
    return test

def serialize_test_options():
    if NAME_DATA_BASE in ['postgres']:
        status = list(db.session.execute(db.select(TestStatus)).scalars())
        subject = list(db.session.execute(db.select(TestSubj)).scalars())
        regname = list(db.session.execute(db.select(Regname)).scalars())
    else:
        status = list(mongo_db.test_status.find())
        subject = list(mongo_db.test_subject.find())
        regname = list(mongo_db.regname.find())
    return {
        "status": status,
        "subject": subject,
        "ptregname": regname,
    }

def serialize_test_columns(exclude=None):
    if NAME_DATA_BASE in ['postgres']:
        cols = list(map(lambda c: c.name, Test.__table__.columns))
        cols = [i if i != "subject" else "subject" for i in cols]
        cols = [i if i != "status" else "status" for i in cols]
        cols = [i if i != "ptregname_id" else "ptregname" for i in cols]
        if exclude:
            cols = list(filter(lambda x: x not in exclude, cols))
    else:
        cols = list(map(lambda c: c.name, Test.__table__.columns))
        if exclude:
            cols = list(filter(lambda x: x not in exclude, cols))
    return cols

def create_test(person_uuid, form):
    data = dict(form)
    test = Test(**data)
    if NAME_DATA_BASE in ['postgres']:
        person = person_service.serialize_person(person_uuid)
        person.tests.append(test)
        db.session.add(person)
        db.session.commit()
    else:
        tests_collection = mongo_db['test']
        test_dict = test.__dict__
        test_dict.pop("_sa_instance_state", None)
        tests_collection.update_one({"uuid": person_uuid}, {"$push": {"test": test_dict}})

        
def update_test(id, form):
    data = dict(form)
    if NAME_DATA_BASE in ['postgres']:
        data = {k:v for k,v in data.items() if v}
        db.session.execute(db.update(Test).filter(Test.id == id).values(**data))
        db.session.commit()
    else:
        data = {k:v for k,v in data.items() if v}
        mongo_db.test.update_one({"id": id}, {"$set": data})
    
def delete_test(id):
    if NAME_DATA_BASE in ['postgres']:
        test = db.one_or_404(db.select(Test).filter(Test.id == id))
        db.session.delete(test)
        db.session.commit()
    else:
        test = test = db.find_one({"id": id}).find_one({"id": id})
    
def query(form):
    data = dict(form)
    
    if result := r.get(str(data)):
        result = pickle.loads(result)
        return result
    
    if NAME_DATA_BASE in ['postgres']:
        result = db.session.execute(
            db.select(Test.year, Regname.name.label("ptregname"), func.min(Test.ball100).label("bmin"))
            .join(Regname)
            .where(
                (Test.ball100 >= 100),
                (Test.ptregname_id == int(data.get("ptregname_id")) if data.get("ptregname_id") else True),
                (Test.subject_id == int(data.get("subject")) if data.get("subject") else True),
                (Test.year == int(data.get("year")) if data.get("year") else True),
            ).group_by(Test.year, Regname.name)
        ).mappings()
        result = list(result)
    else:
        pipeline = [
            {
                "$match": {
                    "ball100": {"$gte": 100},
                    "$or": [
                        {"ptregname_id": int(data.get("ptregname_id"))} if data.get("ptregname_id") else {},
                        {"subject_id": int(data.get("subject"))} if data.get("subject") else {},
                        {"year": int(data.get("year"))} if data.get("year") else {},
                    ],
                }
            },
            {
                "$group": {
                    "_id": {"year": "$year", "ptregname": "$ptregname"},
                    "ptregname": {"$first": "$ptregname"},
                    "year": {"$first": "$year"},
                    "bmin": {"$min": "$ball100"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "year": 1,
                    "ptregname": 1,
                    "bmin": 1,
                }
            },
        ]
        result = list(mongo_db.aggregate(pipeline))
        regions = {
            1: 'Вінницька область',
            2: 'Волинська область',
            3: 'Дніпропетровська область',
            4: 'Донецька область',
            5: 'Житомирська область',
            6: 'Закарпатська область',
            7: 'Запорізька область',
            8: 'Івано-Франківська область',
            9: 'Київська область',
            10: 'Кіровоградська область',
            11: 'Луганська область',
            12: 'Львівська область',
            13: 'Миколаївська область',
            14: 'м. Київ',
            15: 'Одеська область',
            16: 'Полтавська область',
            17: 'Рівненська область',
            18: 'Сумська область',
            19: 'Тернопільська область',
            20: 'Харківська область',
            21: 'Херсонська область',
            22: 'Хмельницька область',
            23: 'Черкаська область',
            24: 'Чернівецька область',
            25: 'Чернігівська область'
        }

        for sublist in result:
            sublist[1] = regions[sublist[1]]
                
    r.set(str(data), pickle.dumps(result))
    
    return result