import pickle
from sqlalchemy.sql import func
from app import db, r
from app.models import Test, TestStatus, TestSubj, Regname
from . import person as person_service

def serialize_test_all(person_uuid):
    tests = db.session.execute(db.select(Test).filter(Test.outid == person_uuid)).scalars()
    return tests

def serialize_test(id):
    test = db.one_or_404(db.select(Test).filter(Test.id == id))
    return test

def serialize_test_options():
    status = list(db.session.execute(db.select(TestStatus)).scalars())
    subject = list(db.session.execute(db.select(TestSubj)).scalars())
    regname = list(db.session.execute(db.select(Regname)).scalars())
    year = list(db.session.execute(db.select(Test.year).distinct()).scalars())
    return {
        "status": status,
        "subject": subject,
        "ptregname": regname,
        "year": year
    }

def serialize_test_columns(exclude=None):
    cols = list(map(lambda c: c.name, Test.__table__.columns))
    cols = [i if i != "subject" else "subject" for i in cols]
    cols = [i if i != "status" else "status" for i in cols]
    cols = [i if i != "ptregname_id" else "ptregname" for i in cols]
    if exclude:
        cols = list(filter(lambda x: x not in exclude, cols))
    return cols

def create_test(person_uuid, form):
    data = dict(form)
    test = Test(**data)
    person = person_service.serialize_person(person_uuid)
    person.tests.append(test)
    db.session.add(person)
    db.session.commit()
        
def update_test(id, form):
    data = dict(form)
    data = {k:v for k,v in data.items() if v}
    db.session.execute(db.update(Test).filter(Test.id == id).values(**data))
    db.session.commit()
    
def delete_test(id):
    test = db.one_or_404(db.select(Test).filter(Test.id == id))
    db.session.delete(test)
    db.session.commit()
    
def query(form):
    data = dict(form)
    
    if result := r.get(str(data)):
        result = pickle.loads(result)
        return result
    
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

    r.set(str(data), pickle.dumps(result))
    
    return result