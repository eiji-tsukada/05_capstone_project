from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

database_name = 'custing'
database_path = 'postgres://{}{}'.format('localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    """ binds a flask application and a SQLAlchemy service """
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def __repr__(self):
        return 'Movie ID:{} | Title: {}'.format(self.id, self.title)


class Actor(db.Model):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String(10))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return 'Actor ID:{} | Name: {}'.format(self.id, self.name)
