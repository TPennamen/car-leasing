import datetime

from .test_base import BasicTestCase



class OrderTest(BasicTestCase):
    def setUp(self) -> None:
        super().setUp()
        data = {'email': 'test@test.com', 'firstname': 'firstname_test', 'lastname': 'lastname_test'}
        self.client.post('/api/customers', data=data)

    def get_data(self):
        return {'customer_id': 1, 'car_id': 1,
                'start_datetime': datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
                'end_datetime': datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(hours=2),
                                                           '%Y-%m-%d %H:%M:%S')}

    def test_get_all_empty(self):
        response = self.client.get('/api/orders')
        self.assert200(response)
        self.assertEqual(response.json, [])

    def test_post_one_will_passed(self):
        data = self.get_data()
        response = self.client.post('/api/orders', data=data)
        self.assertEqual(response.status, '201 CREATED')

    def test_post_one_will_failed_bad_request(self):
        data = self.get_data()
        data['start_datetime'] = None
        response = self.client.post('/api/orders', data=data)
        self.assertEqual(response.status, '400 BAD REQUEST')

    def test_get_all_one_example(self):
        data = self.get_data()
        self.client.post('/api/orders', data=data)
        response = self.client.get('/api/orders')
        self.assert200(response)
        self.assertEqual(len(response.json), 1)

        order_created = response.json[0]
        self.assertIsNotNone(order_created['id'])
        self.assertEqual(order_created['customer']['id'], 1)

    def test_get_by_id_one_example(self):
        self.test_post_one_will_passed()
        response = self.client.get('/api/orders/1')
        self.assert200(response)

        order_created = response.json
        self.assertIsNotNone(order_created['id'])
        self.assertEqual(order_created['customer']['id'], 1)

    def test_get_by_id_one_example_failed(self):
        response = self.client.get('/api/orders/1')
        self.assert404(response)

    def test_put_by_id_on_example(self):
        self.test_post_one_will_passed()
        data = self.get_data()
        data['car_id'] = 2
        response = self.client.put('/api/orders/1', data=data)
        self.assert200(response)
        response = self.client.get('/api/orders/1')
        order_created = response.json
        self.assertIsNotNone(order_created['id'])
        self.assertEqual(order_created['car']['id'], 2)

    def test_delete_by_id(self):
        self.test_post_one_will_passed()
        response = self.client.delete('/api/orders/1')
        self.assert200(response)
        self.test_get_by_id_one_example_failed()