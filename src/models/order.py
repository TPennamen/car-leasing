from .shared import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, car, customer, start_datetime, end_datetime):
        assert end_datetime > start_datetime

        self.car_id = car.id
        self.customer_id = customer.id
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.price = (end_datetime - start_datetime).seconds / 3600 * car.price_per_hour
