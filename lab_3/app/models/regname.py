from app import db

class Regname(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    def __str__(self):
        return self.name
    