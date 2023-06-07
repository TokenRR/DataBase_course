from app import db


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    outid = db.Column(db.UUID, db.ForeignKey("person.outid"))
    year = db.Column(db.Integer)
    subject_id = db.Column(db.ForeignKey("test_subj.id", ondelete="cascade"))
    status_id = db.Column(db.ForeignKey("test_status.id", ondelete="cascade"))
    ball100 = db.Column(db.Integer)
    ball12 = db.Column(db.Integer)
    ball = db.Column(db.Integer)
    ptname = db.Column(db.String)
    ptregname_id = db.Column(db.ForeignKey("regname.id", ondelete="cascade"))
    ptareaname = db.Column(db.String)
    pttername = db.Column(db.String)
    person = db.relationship("Person", single_parent=True, back_populates="tests")
    subject = db.relationship("TestSubj", lazy=True)
    status = db.relationship("TestStatus", lazy=True)
    ptregname = db.relationship("Regname", lazy=True)


    def to_dict(self):
        return {
            'id': self.id,
            'outid': str(self.outid),
            'year': self.year,
            'subject_id': self.subject_id,
            'status_id': self.status_id,
            'ball100': self.ball100,
            'ball12': self.ball12,
            'ball': self.ball,
            'ptname': self.ptname,
            'ptregname_id': self.ptregname_id,
            'ptareaname': self.ptareaname,
            'pttername': self.pttername
        }