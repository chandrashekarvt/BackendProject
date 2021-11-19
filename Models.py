from app import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


# Defining the database table in the form of a class model
class SearchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    thumbnail = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return '<Item %r>' % self.id
