from datetime import datetime
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
        return {
        'id': self.id,
        'name': self.name,
        'category': self.category,
        'description': self.description,
        'created_date': self.created_date.strftime("%Y-%m-%d %H:%M:%S"),
        'last_edit_date': self.last_edit_date.strftime("%Y-%m-%d %H:%M:%S"),
        'image': self.image,
        'rate': self.rate
        }

    def json_response(self):
        return {
        'id': self.id,
        'image': self.image,
        'rate': self.rate,
        }

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

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
