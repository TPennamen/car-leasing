from .test_base import BasicTestCase


class CustomerTest(BasicTestCase):
    def test_get_all_empty(self):
        response = self.client.get('/api/customers')
        self.assert200(response)
        self.assertEqual(response.json, [])

    def test_post_one_will_passed(self):
        data = {'email': 'test@test.com', 'firstname': 'firstname_test', 'lastname': 'lastname_test'}
        response = self.client.post('/api/customers', data=data)
        self.assertEqual(response.status, '201 CREATED')

    def test_post_one_will_failed_bad_request(self):
        data = {'firstname': 'firstname_test', 'lastname': 'lastname_test'}
        response = self.client.post('/api/customers', data=data)
        self.assertEqual(response.status, '400 BAD REQUEST')

    def test_post_one_will_failed_already_exists(self):
        data = {'email': 'test@test.com', 'firstname': 'firstname_test', 'lastname': 'lastname_test'}
        self.client.post('/api/customers', data=data)
        response = self.client.post('/api/customers', data=data)
        self.assertEqual(response.status, '403 FORBIDDEN')

    def test_get_all_one_example(self):
        data = {'email': 'test@test.com', 'firstname': 'firstname_test', 'lastname': 'lastname_test'}
        self.client.post('/api/customers', data=data)
        response = self.client.get('/api/customers')
        self.assert200(response)
        self.assertEqual(len(response.json), 1)

        customer_created = response.json[0]
        self.assertIsNotNone(customer_created['id'])
        self.assertEqual(customer_created['email'], 'test@test.com')

    def test_get_by_id_one_example(self):
        self.test_post_one_will_passed()
        response = self.client.get('/api/customers/1')
        self.assert200(response)

        customer_created = response.json
        self.assertIsNotNone(customer_created['id'])
        self.assertEqual(customer_created['email'], 'test@test.com')

    def test_get_by_id_one_example_failed(self):
        response = self.client.get('/api/customers/1')
        self.assert404(response)

    def test_put_by_id_on_example(self):
        self.test_post_one_will_passed()
        data = {'email': 'test@test.com', 'firstname': 'firstname_modified', 'lastname': 'lastname_test'}
        response = self.client.put('/api/customers/1', data=data)
        self.assert200(response)
        response = self.client.get('/api/customers/1')
        customer_created = response.json
        self.assertIsNotNone(customer_created['id'])
        self.assertEqual(customer_created['firstname'], 'firstname_modified')

    def test_delete_by_id(self):
        self.test_post_one_will_passed()
        response = self.client.delete('/api/customers/1')
        self.assert200(response)
        self.test_get_by_id_one_example_failed()