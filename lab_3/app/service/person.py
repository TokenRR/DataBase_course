from app import db
from app.models import Person, SexType, Regname
from sqlalchemy import func

def serialize_person_all_desc():
    persons = db.paginate(db.select(Person).order_by(Person.birth.desc()), per_page=5)
    return persons

def serialize_person_all_asc():
    persons = db.paginate(db.select(Person).order_by(Person.birth.asc()), per_page=5)
    return persons

def serialize_person(uuid):
    person = db.one_or_404(db.select(Person).filter(Person.outid == uuid))
    return person

def serialize_person_options():
    sextype = list(db.session.execute(db.select(SexType)).scalars())
    regname = list(db.session.execute(db.select(Regname)).scalars())
    return {
        "sextype": sextype,
        "regname": regname,
    }

def create_person(form):
    data = dict(form)
    db.session.add(Person(**data))
    db.session.commit()

def update_person(uuid, form):
    data = dict(form)
    data = {k:v for k,v in data.items() if v}
    db.session.execute(db.update(Person).filter(Person.outid == uuid).values(**data))
    db.session.commit()

def delete_person(uuid):
    person = db.one_or_404(db.select(Person).filter(Person.outid == uuid))
    db.session.delete(person)
    db.session.commit()

def serialize_person_columns(exclude=None):
    cols = list(map(lambda c: c.name, Person.__table__.columns))
    cols = [i if i != "sextype_id" else "sextype" for i in cols]
    cols = [i if i != "regname_id" else "regname" for i in cols]
    if exclude is not None:
        cols = list(filter(lambda x: x not in exclude, cols))
    return cols