from app import db
from app.models import Person, SexType, Regname
from sqlalchemy import func
from app import NAME_DATA_BASE, mongo_db


def serialize_person_all_desc():
    if NAME_DATA_BASE in ['postgres']:
        persons = db.paginate(db.select(Person).order_by(Person.birth.desc()), per_page=5)
    else:
        persons = mongo_db.person.find().sort('birth', -1).limit(5);
    return persons

def serialize_person_all_asc():
    if NAME_DATA_BASE in ['postgres']:
        persons = db.paginate(db.select(Person).order_by(Person.birth.asc()), per_page=5)
    else:
        persons = mongo_db.person.find().sort('birth', 1).limit(5);
    return persons

def serialize_person(uuid):
    if NAME_DATA_BASE in ['postgres']:
        person = db.one_or_404(db.select(Person).filter(Person.outid == uuid))
    else:
        person = mongo_db.person.find_one({"outid": uuid})
    return person

def serialize_person_options():
    if NAME_DATA_BASE in ['postgres']:
        sextype = list(db.session.execute(db.select(SexType)).scalars())
        regname = list(db.session.execute(db.select(Regname)).scalars())
    else:
        sextype_collection = mongo_db['sextype']
        regname_collection = mongo_db['regname']

        sextype = list(sextype_collection.find())
        regname = list(regname_collection.find())
    return {
        "sextype": sextype,
        "regname": regname,
    }

def create_person(form):
    data = dict(form)
    if NAME_DATA_BASE in ['postgres']:
        db.session.add(Person(**data))
        db.session.commit()
    else:
        mongo_db.insert_one(data)

def update_person(uuid, form):
    data = dict(form)
    if NAME_DATA_BASE in ['postgres']:
        data = {k:v for k,v in data.items() if v}
        db.session.execute(db.update(Person).filter(Person.outid == uuid).values(**data))
        db.session.commit()
    else:
        data = {k:v for k,v in data.items() if v}
        mongo_db.person.update_one({"outid": uuid}, {"$set": data})


def delete_person(uuid):
    if NAME_DATA_BASE in ['postgres']:
        person = db.one_or_404(db.select(Person).filter(Person.outid == uuid))
        db.session.delete(person)
        db.session.commit()
    else:
        person = mongo_db.person.find_one({"outid": uuid})


def serialize_person_columns(exclude=None):
    if NAME_DATA_BASE in ['postgres']:
        cols = list(map(lambda c: c.name, Person.__table__.columns))
        cols = [i if i != "sextype_id" else "sextype" for i in cols]
        cols = [i if i != "regname_id" else "regname" for i in cols]
        if exclude is not None:
            cols = list(filter(lambda x: x not in exclude, cols))
    else:
        cols = list(map(lambda c: c.name, Person.__table__.columns))
        if exclude is not None:
            cols = list(filter(lambda x: x not in exclude, cols))
    return cols