from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates

from app import db


class ItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    category = db.Column(db.String(), default = "movie")
    description = db.Column(db.Text())
    created_date = db.Column(db.DateTime(), default=datetime.utcnow)
    last_edit_date = db.Column(db.DateTime(), default=datetime.utcnow)
    image = db.Column(db.String())
    rate = db.Column(db.Integer, default=1)

    def json(self):
        json = {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'created_date': self.created_date.strftime("%Y-%m-%d %H:%M:%S"),
            'last_edit_date': self.last_edit_date.strftime("%Y-%m-%d %H:%M:%S"),
            'rate': self.rate
        }
        if self.description:
            json['description'] = self.description
        if self.image:
            json['image'] = self.image
        return json

    def json_response(self):
        json = {
            'id': self.id,
            'created_date': self.created_date.strftime("%Y-%m-%d %H:%M:%S"),
            'rate': self.rate,
        }
        if self.image:
            json['image'] = self.image
        return json

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    def delete_image(self):
        self.image = None
        # надо искать в bucket картинку и удалять

    def update_last_edit_date(self):
        self.last_edit_date = datetime.utcnow()

    def update_fields(self, save=False, **fields):
        for field, value in fields.items():
            # There's just one and only category
            if field == 'category': continue
            if hasattr(self, field):
                setattr(self, field, value)
        self.update_last_edit_date()
        if save:
            self.save()

    def __repr__(self):
        return "ItemModel {}".format(self.name)


    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, item_id):
        return cls.query.filter_by(id=item_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


class CategoryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    color = db.Column(db.Integer())


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "UserModel id={}, username={}".format(self.id, self.username)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filer_by(id=id)
