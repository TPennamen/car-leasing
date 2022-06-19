from .test_base import BasicTestCase
from src.models import Car


class CarTest(BasicTestCase):
    def test_get_all(self):
        response = self.client.get('/api/cars')
        self.assert200(response)
        self.assertEqual(response.json,
                         [{'id': '1', 'brand': 'Porsche', 'model': '911', 'price_per_hour': '150', 'orders': []},
                          {'id': '2', 'brand': 'Peugeot', 'model': '307', 'price_per_hour': '40', 'orders': []},
                          {'id': '3', 'brand': 'Renault', 'model': 'Twingo', 'price_per_hour': '30', 'orders': []},
                          {'id': '4', 'brand': 'Renault', 'model': 'Scenic', 'price_per_hour': '60', 'orders': []},
                          {'id': '5', 'brand': 'Tesla', 'model': 'X', 'price_per_hour': '120', 'orders': []},
                          {'id': '6', 'brand': 'Citroën', 'model': 'C3', 'price_per_hour': '35', 'orders': []},
                          {'id': '7', 'brand': 'Renault', 'model': 'Traffic', 'price_per_hour': '90', 'orders': []},
                          {'id': '8', 'brand': 'Alpha Roméo', 'model': 'Giulietta', 'price_per_hour': '100',
                           'orders': []},
                          {'id': '9', 'brand': 'Fiat', 'model': 'Multipla', 'price_per_hour': '120', 'orders': []},
                          {'id': '10', 'brand': 'Mini', 'model': 'Countryman', 'price_per_hour': '60', 'orders': []}])

    def test_post_one_will_passed(self):
        data = {'brand': 'brand', 'model': 'model_test', 'price_per_hour': 20}
        response = self.client.post('/api/cars', data=data)
        self.assertEqual(response.status, '201 CREATED')
        car_inserted = Car.query.filter_by(brand='brand').first()
        self.assertIsNotNone(car_inserted)

    def test_post_will_failed_price_in_string(self):
        data = {'brand': 'brand', 'model': 'model_test', 'price_per_hour': 'price_test_in_string'}
        response = self.client.post('/api/cars', data=data)
        self.assert400(response)

    def test_post_will_failed_bad_args(self):
        data = {'model': 'model_test', }
        response = self.client.post('/api/cars', data=data)
        self.assert400(response)

    def test_get_by_id_one_example(self):
        self.test_post_one_will_passed()
        response = self.client.get('/api/cars/11')
        self.assert200(response)

        car_created = response.json
        self.assertIsNotNone(car_created['id'])
        self.assertEqual(car_created['brand'], 'brand')

    def test_get_by_id_one_example_failed(self):
        response = self.client.get('/api/cars/111')
        self.assert404(response)

    def test_put_by_id_on_example(self):
        self.test_post_one_will_passed()
        data = {'brand': 'brand', 'model': 'model_modified', 'price_per_hour': 20}
        response = self.client.put('/api/cars/11', data=data)
        self.assert200(response)
        response = self.client.get('/api/cars/11')
        car_created = response.json
        self.assertIsNotNone(car_created['id'])
        self.assertEqual(car_created['model'], 'model_modified')

    def test_delete_by_id(self):
        self.test_post_one_will_passed()
        response = self.client.delete('/api/cars/11')
        self.assert200(response)
        self.test_get_by_id_one_example_failed()
