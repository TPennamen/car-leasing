
from flask_restx import Namespace, Resource, fields, reqparse
from ..models import db, Car

car_api = Namespace('cars', description='Cars related operations')

order_dto = car_api.model('Order', {
    'id': fields.Integer(required=True),
    'start_datetime': fields.DateTime(required=True),
    'end_datetime': fields.DateTime(required=True),
    'price': fields.Integer(required=True)
})

car_dto = car_api.model('Car', {
    'id': fields.String(required=True, description='The car identifier'),
    'brand': fields.String(required=True, description='The car brand'),
    'model': fields.String(required=True, description='The car model'),
    'price_per_hour': fields.String(required=True, description='The car price per hour of use'),
    'orders': fields.List(fields.Nested(model=order_dto, allow_null=True))
})

car_parser = reqparse.RequestParser()
car_parser.add_argument('brand', type=str, location='form', required=True)
car_parser.add_argument('model', type=str, location='form', required=True)
car_parser.add_argument('price_per_hour', type=int, location='form', required=True)


@car_api.route('')
class CarListResource(Resource):
    @car_api.doc('list_cars')
    @car_api.marshal_list_with(car_dto)
    def get(self):
        """List all cars"""
        return Car.query.all()

    @car_api.doc('add_car')
    @car_api.expect(car_parser)
    def post(self):
        """Create a car"""
        body = car_parser.parse_args()

        new_car = Car(brand=body['brand'],
                      model=body['model'],
                      price_per_hour=body['price_per_hour'])
        db.session.add(new_car)
        db.session.commit()

        return 'Created', 201


@car_api.route('/<int:car_id>')
@car_api.param('car_id', 'The car identifier')
class CarResource(Resource):
    @car_api.doc('get_car')
    @car_api.marshal_with(car_dto)
    def get(self, car_id):
        """Fetch a car given its identifier"""
        car_chosen = Car.query.filter_by(id=car_id).first()
        if car_chosen is None:
            car_api.abort(404)
        return car_chosen

    @car_api.doc('update_car')
    @car_api.expect(car_parser)
    def put(self, car_id):
        """Update a car given its identifier"""

        body = car_parser.parse_args()
        car_chosen = Car.query.filter_by(id=car_id).update(body)
        if car_chosen is None:
            car_api.abort(404)

        db.session.commit()

    @car_api.doc('delete_car')
    def delete(self, car_id):
        """Fetch a car given its identifier"""
        car_chosen = Car.query.filter_by(id=car_id).first()
        if car_chosen is None:
            car_api.abort(404)
        db.session.delete(car_chosen)
        db.session.commit()
