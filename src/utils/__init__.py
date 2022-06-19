import datetime

from ..models import Order, Car, Customer


def datetime_parser(str_datetime):
    assert str_datetime is not None
    return datetime.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S").replace(minute=0, second=0, microsecond=0)


def add_customer_and_car_to_order(order: Order, customer: Customer, car: Car) -> dict:
    assert order is not None
    assert customer is not None
    assert car is not None

    return {'id': order.id, 'start_datetime': order.start_datetime, 'end_datetime': order.end_datetime,
            'price': order.price, 'customer': customer, 'car': car}
