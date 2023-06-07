from app import db

class SexType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    
    def __str__(self):
        return self.type
    