from random import randint
from faker import Faker
from app.models import ItemModel
from app import db

if __name__ == '__main__':
    fake = Faker()
    db.create_all()
    for e in range(30):
        f_name = fake.sentence(nb_words=3)
        f_category = fake.word()
        f_description = fake.sentence()[:-1]
        f_created_date = fake.date()
        f_last_edit_date = fake.date()
        f_image = fake.file_name(category='image')
        f_rate = randint(1,100)
        item = ItemModel(
            name=f_name, 
            category=f_category,
            description=f_description,
            created_date=f_created_date,
            last_edit_date=f_last_edit_date,
            image=f_image,
            rate=f_rate,
            )
        db.session.add(item)
    db.session.commit()
    print("Database populated")

