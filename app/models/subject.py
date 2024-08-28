# app/models/subject.py
from sqlalchemy.sql.operators import truediv

from __init__ import db

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user = db.Column(db.String(100), nullable=True)
    pid = db.Column(db.Integer, nullable=True)
    stage_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Post({self.user}, {self.pid}, {self.stage_id}, '{self.title}')"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "user": self.user,
            "pid": self.pid,
            "stage_id": self.stage_id,
        }