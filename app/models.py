from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"{self.username} ({self.email})"
