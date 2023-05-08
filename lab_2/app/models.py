'''*_*'''

 
import uuid
from app import db


class SexType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)


class Regname(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class TestStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)


class TestSubj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Person(db.Model):
    outid = db.Column(db.UUID, primary_key=True, default = uuid.uuid4)
    birth = db.Column(db.Integer)
    sextype_id = db.Column(db.ForeignKey('sex_type.id', ondelete='cascade'))
    regname_id = db.Column(db.ForeignKey('regname.id', ondelete='cascade'))
    areaname = db.Column(db.String)
    tername = db.Column(db.String)
    regtypename = db.Column(db.String)
    tertypename = db.Column(db.String)
    classprofilename = db.Column(db.String)
    classlangname = db.Column(db.String)
    eoname = db.Column(db.String)
    eotypename = db.Column(db.String)
    eoregname = db.Column(db.String)
    eoareaname = db.Column(db.String)
    eotername = db.Column(db.String)
    eoparent = db.Column(db.String)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    outid = db.Column(db.ForeignKey('person.outid', ondelete='cascade'), default = uuid.uuid4)
    year = db.Column(db.Integer)
    subject_id = db.Column(db.ForeignKey('test_subj.id', ondelete='cascade'))
    status_id = db.Column(db.ForeignKey('test_status.id', ondelete='cascade'))
    ball100 = db.Column(db.DOUBLE_PRECISION)
    ball12 = db.Column(db.Integer)
    ball = db.Column(db.String)
    ptname = db.Column(db.String)
    ptregname_id = db.Column(db.ForeignKey('regname.id', ondelete='cascade'))
    ptareaname = db.Column(db.String)
    pttername = db.Column(db.String)
