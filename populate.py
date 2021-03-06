from random import randint
from faker import Faker
from app.models import ItemModel
from app import db

if __name__ == '__main__':
    fake = Faker()
    db.create_all()
    for e in range(30):
        f_name = fake.sentence(nb_words=3)[:-1]
        f_description = fake.sentence()
        f_created_date = fake.date_time()
        f_last_edit_date = fake.date_time_between_dates(datetime_start=f_created_date)
        f_rate = randint(1,100)
        item = ItemModel(
            name=f_name, 
            description=f_description,
            created_date=f_created_date,
            last_edit_date=f_last_edit_date,
            rate=f_rate,
            )
        db.session.add(item)
    db.session.commit()
    print("Database populated")

