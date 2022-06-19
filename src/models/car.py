from .shared import db


class Car(db.Model):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(128), nullable=False)
    model = db.Column(db.String(128), nullable=False)
    price_per_hour = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', backref='cars', cascade="all, delete")

    def __init__(self, brand, model, price_per_hour):
        self.brand = brand
        self.model = model
        self.price_per_hour = price_per_hour


