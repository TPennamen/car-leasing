import json

from flask_testing import TestCase
from src import app, db
from src.models import Car


class BasicTestCase(TestCase):
    def setUp(self) -> None:
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            with open(file="src/seeds/cars.json") as json_file:
                data = json.load(json_file)
                cars = data['cars']
                for car in cars:
                    db.session.add(Car(brand=car['brand'], model=car['model'],
                                       price_per_hour=car['price_per_hour']))

                db.session.commit()

    def create_app(self):
        app.config.from_object('src.config.TestConfig')

        return app
