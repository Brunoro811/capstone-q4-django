from operator import itemgetter

from rest_framework.test import APITestCase

from ..utils import user_admin_correct, user_seller_correct


class TestAccounst(APITestCase):
    @classmethod
    def setUpTestData(cls):
        email, password = itemgetter('email', 'password')(user_admin_correct)
        admin_login_info = {'email': email, 'password': password}
        email, password = itemgetter('email', 'password')(user_seller_correct)
        seller_login_info = {'email': email, 'password': password}
        cls.admin_login_info = admin_login_info
        cls.seller_login_info = seller_login_info
        cls.admin_register_info = user_admin_correct
        cls.seller_register_info = user_seller_correct

    def test_cant_list_all_without_being_logged(self):
        response = self.client.get('/api/accounts/', format='json')

        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.json())

    def test_can_list_all_users_as_admin(self):
        self.client.post('/api/accounts/', self.admin_register_info, format='json')
        token = self.client.post(
            '/api/login/', self.admin_login_info, format='json'
        ).json()['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/accounts/', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_cant_list_all_users_as_seller(self):
        self.client.post('/api/accounts/', self.seller_register_info, format='json')
        token = self.client.post(
            '/api/login/', self.admin_login_info, format='json'
        ).json()['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.get('/api/accounts/', format='json')

        self.assertEqual(response.status_code, 403)
        self.assertIn('detail', response.json())
