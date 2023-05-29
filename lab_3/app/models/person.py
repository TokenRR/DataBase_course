import uuid
from app import db


class Person(db.Model):
    outid = db.Column(db.UUID, primary_key = True, default = uuid.uuid4)
    birth = db.Column(db.Integer)
    sextype_id = db.Column(db.ForeignKey("sex_type.id", ondelete="cascade"))
    regname_id = db.Column(db.ForeignKey("regname.id", ondelete="cascade"))
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
    tests = db.relationship("Test", cascade="all,delete-orphan", lazy=True, back_populates="person")
    sextype = db.relationship("SexType", lazy=True)
    regname = db.relationship("Regname", lazy=True)
    