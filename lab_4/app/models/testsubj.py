from app import db

class TestSubj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    def __str__(self):
        return self.name
    