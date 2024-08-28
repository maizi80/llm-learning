from __init__ import db

class Learn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    hid = db.Column(db.Integer, nullable=False)
    oid = db.Column(db.Integer, nullable=False)
    bid = db.Column(db.Integer, nullable=False)
    sid = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Learn({self.user}, {self.pid}, {self.hid}, '{self.oid}', '{self.bid}', '{self.sid}')"

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user,
            "pid": self.pid,
            "hid": self.hid,
            "oid": self.oid,
            "bid": self.bid,
            "sid": self.sid
        }