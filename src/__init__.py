from flask import Flask
from flask_restx import Api

from .models import db
from .resources import customer_api, car_api, order_api

app = Flask(__name__)
app.config.from_object("src.config.Config")
db.init_app(app)


api = Api(
    title='Car leasing',
    version='1.0',
    description='Car leasing api',
    prefix='/api'
)

api.add_namespace(customer_api, path='/customers')
api.add_namespace(car_api, path='/cars')
api.add_namespace(order_api, path='/orders')

api.init_app(app)
