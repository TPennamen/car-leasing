import json
import random
import datetime

from flask.cli import FlaskGroup

from src import app
from src.models import db, Car, Customer, Order

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        with open(file="src/seeds/cars.json") as json_file:
            data = json.load(json_file)
            cars = data['cars']
            for car in cars:
                db.session.add(Car(brand=car['brand'], model=car['model'],
                                   price_per_hour=car['price_per_hour']))

            db.session.commit()


@cli.command("seed_db")
def seed_db():
    with open(file="src/seeds/customers.json") as json_file:
        data = json.load(json_file)
        new_customers = data['customers']
        for customer in new_customers:
            db.session.add(Customer(email=customer['email'],
                                    firstname=customer['firstname'],
                                    lastname=customer['lastname']))
        customers = Customer.query.all()
        cars = Car.query.all()

        for order_index in range(10):
            customer_chosen = random.choice(customers)
            car_chosen = random.choice(cars)
            start_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0) \
                         + datetime.timedelta(hours=random.randint(-200, 200))
            new_order = Order(car=car_chosen, customer=customer_chosen,
                              start_datetime=start_time,
                              end_datetime=(start_time + datetime.timedelta(hours=random.randint(1, 10))))
            db.session.add(new_order)
        db.session.commit()


if __name__ == "__main__":
    cli()
