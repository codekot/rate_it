from app import db


class ItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    category = db.Column(db.String())
    description = db.Column(db.Text())
    created_date = db.Column(db.String())
    last_edit_date = db.Column(db.String())
    image = db.Column(db.String())
    rate = db.Column(db.Integer)

    def json(self):
        return {
        'id': self.id,
        'name': self.name,
        'category': self.category,
        'description': self.description,
        'created_date': self.created_date,
        'last_edit_date': self.last_edit_date,
        'image': self.image,
        'rate': self.rate
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, item_id):
        return cls.query.filter_by(id=item_id).first()


class CategoryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    color = db.Column(db.Integer())
