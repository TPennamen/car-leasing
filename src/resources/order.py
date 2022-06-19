import datetime

from flask_restx import Namespace, Resource, fields, reqparse
from ..models import db, Order, Car, Customer
from ..utils import datetime_parser, add_customer_and_car_to_order

order_api = Namespace('orders', description='Orders related operations')

customer_dto = order_api.model('Customer', {
    'id': fields.Integer(required=True, description='The customer identifier'),
    'email': fields.String(required=True, description='The customer name'),
    'firstname': fields.String(required=True, description='The customer name'),
    'lastname': fields.String(required=True, description='The customer name'),
})

car_dto = order_api.model('Car', {
    'id': fields.Integer(required=True, description='The car identifier'),
    'brand': fields.String(required=True, description='The car brand'),
    'model': fields.String(required=True, description='The car model'),
    'price_per_hour': fields.Integer(required=True, description='The car price per hour of use'),
})

order_dto = order_api.model('Order', {
    'id': fields.Integer(required=True),
    'start_datetime': fields.DateTime(required=True),
    'end_datetime': fields.DateTime(required=True),
    'price': fields.Integer(required=True),
    'customer': fields.Nested(customer_dto),
    'car': fields.Nested(car_dto)
})

order_parser = reqparse.RequestParser()
order_parser.add_argument('car_id', type=int, location='form', required=True)
order_parser.add_argument('customer_id', type=int, location='form', required=True)
order_parser.add_argument('start_datetime', type=datetime_parser, location='form', required=True)
order_parser.add_argument('end_datetime', type=datetime_parser, location='form', required=True)


@order_api.route('')
class OrderList(Resource):
    @order_api.doc('list_orders')
    @order_api.marshal_list_with(order_dto)
    def get(self):
        """List all orders"""
        orders = Order.query.all()
        customer_ids = map(lambda o: o.customer_id, orders)
        car_ids = map(lambda o: o.car_id, orders)

        cars = Car.query.filter(Car.id.in_(car_ids)).all()
        customers = Customer.query.filter(Customer.id.in_(customer_ids)).all()

        result = []
        for order in orders:
            order_car = [c for c in cars if c.id == order.car_id][0]
            order_customer = [c for c in customers if c.id == order.customer_id][0]
            result.append(add_customer_and_car_to_order(order, order_customer, order_car))

        return result

    @order_api.doc('add_order')
    @order_api.expect(order_parser)
    def post(self):
        """Create a order"""
        body = order_parser.parse_args()
        car_chosen = Car.query.filter_by(id=body['car_id']).first()
        customer_chosen = Customer.query.filter_by(id=body['customer_id']).first()
        if car_chosen is None or customer_chosen is None:
            order_api.abort(404)

        db.session.add(Order(car_chosen, customer_chosen,body['start_datetime'], body['end_datetime']))
        db.session.commit()
        return 'Created', 201


@order_api.route('/<order_id>')
@order_api.param('order_id', 'The order identifier')
@order_api.response(404, 'Order not found')
class OrderResource(Resource):
    @order_api.doc('get_order')
    @order_api.marshal_with(order_dto)
    def get(self, order_id):
        """Fetch a order given its identifier"""
        order_chosen = Order.query.filter_by(id=order_id).first()
        if order_chosen is None:
            order_api.abort(404)

        order_car = Car.query.filter_by(id=order_chosen.car_id).first()
        order_customer = Customer.query.filter_by(id=order_chosen.customer_id).first()

        return add_customer_and_car_to_order(order_chosen, order_customer, order_car)

    @order_api.doc('update_order')
    @order_api.expect(order_parser)
    def put(self, order_id):
        """Update a order given its identifier"""
        body = order_parser.parse_args()
        if body['start_datetime'] >= body['end_datetime']:
            order_api.abort(400)
        order_chosen = Order.query.filter_by(id=order_id).update(body)
        if order_chosen is None:
            order_api.abort(404)

        db.session.commit()

    @order_api.doc('delete_order')
    def delete(self, order_id):
        """Fetch a order given its identifier"""
        order_chosen = Order.query.filter_by(id=order_id).first()
        if order_chosen is None:
            order_api.abort(404)
        db.session.delete(order_chosen)
        db.session.commit()
