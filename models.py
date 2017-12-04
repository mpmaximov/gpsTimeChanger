from app import db
from sqlalchemy.dialects.postgresql import JSON


class Intervals(db.Model):
    __tablename__ = 'intervals'

    id = db.Column(db.Integer, primary_key=True)
    tbegin = db.Column(db.String())
    tend = db.Column(db.String())

    def __repr__(self):
        return '<id {}>'.format(self.id)