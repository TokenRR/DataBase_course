from app import db

class TestStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    
    def __str__(self):
        return self.status