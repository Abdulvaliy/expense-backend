from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(150), nullable=True)
    name = db.Column(db.String(150), nullable=False)
    birthdate = db.Column(db.String(30), nullable=True)
    gender = db.Column(db.String(15), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    currency = db.Column(db.String(15), nullable=False)
    region = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    platform = db.Column(db.String(100), nullable=True)
    registered_date = db.Column(db.String(100), nullable=True)

    def to_dict(self):  # automatic calling the dict (creating a func)
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# flask db init
# flask db migrate
# flask db upgrade
