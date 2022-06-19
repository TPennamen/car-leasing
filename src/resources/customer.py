from flask_restx import Namespace, Resource, fields, reqparse
from ..models import db, Customer
from sqlalchemy.exc import IntegrityError

customer_api = Namespace('customers', description='Customers related operations')

order_dto = customer_api.model('Order', {
    'id': fields.Integer(required=True),
    'start_datetime': fields.DateTime(required=True),
    'end_datetime': fields.DateTime(required=True),
    'price': fields.Integer(required=True)
})

customer_dto = customer_api.model('Customer', {
    'id': fields.String(required=True, description='The customer identifier'),
    'email': fields.String(required=True, description='The customer name'),
    'firstname': fields.String(required=True, description='The customer name'),
    'lastname': fields.String(required=True, description='The customer name'),
    'orders': fields.List(fields.Nested(model=order_dto, allow_null=True))
})

customer_parser = reqparse.RequestParser()
customer_parser.add_argument('email', type=str, location='form', required=True)
customer_parser.add_argument('firstname', type=str, location='form', required=True)
customer_parser.add_argument('lastname', type=str, location='form', required=True)


@customer_api.route('')
class CustomerList(Resource):
    @customer_api.doc('list_customers')
    @customer_api.marshal_list_with(customer_dto)
    def get(self):
        """List all customers"""
        return Customer.query.all()

    @customer_api.doc('insert_customer')
    @customer_api.expect(customer_parser)
    def post(self):
        """Create a customer"""
        body = customer_parser.parse_args()
        try:
            new_customer = Customer(email=body['email'],
                                firstname=body['firstname'],
                                lastname=body['lastname'])

            db.session.add(new_customer)
            db.session.commit()
        except IntegrityError:
            customer_api.abort(403)

        return 'Created', 201


@customer_api.route('/<int:customer_id>')
@customer_api.param('customer_id', 'The customer identifier')
class CustomerResource(Resource):
    @customer_api.doc('get_customer')
    @customer_api.marshal_with(customer_dto)
    def get(self, customer_id):
        """Fetch a customer given its identifier"""
        customer_chosen = Customer.query.filter_by(id=customer_id).first()
        if customer_chosen is None:
            customer_api.abort(404)
        return customer_chosen

    @customer_api.doc('update_customer')
    @customer_api.expect(customer_parser)
    def put(self, customer_id):
        """Update a customer given its identifier"""
        body = customer_parser.parse_args()
        customer_chosen = Customer.query.filter_by(id=customer_id).update(body)
        if customer_chosen is None:
            customer_api.abort(404)

        db.session.commit()

    @customer_api.doc('delete_customer')
    def delete(self, customer_id):
        """Fetch a customer given its identifier"""
        customer_chosen = Customer.query.filter_by(id=customer_id).first()
        if customer_chosen is None:
            customer_api.abort(404)
        db.session.delete(customer_chosen)
        db.session.commit()