from django.test import TestCase
from rest_framework.test import APITestCase
from users.models import User
from rest_framework.authtoken.models import Token
from users.serializer import UserSerializer
from rest_framework.test import APIClient, APITestCase


class UserModelTest(TestCase):
    @classmethod
    def testDataSeller(cls):
        cls.username = "teste"
        cls.password = "1234"
        cls.first_name = "Teste"
        cls.last_name = "Testado"
        cls.is_seller = True
        cls.user = User.objects.create_user(username = cls.username,password=cls.password, first_name=cls.first_name, last_name=cls.last_name, is_seller=cls.is_seller)
    def testDataNotSeller(cls):
        cls.username = "teste"
        cls.password = "1234"
        cls.first_name = "Teste"
        cls.last_name = "Testado"
        cls.is_seller = False
        cls.user = User.objects.create_user(username = cls.username,password=cls.password, first_name=cls.first_name, last_name=cls.last_name, is_seller=cls.is_seller)


class UsersViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super = User.objects.create_superuser(username='superTestm', password='1234', first_name='super', last_name='Manda')
        cls.seller = User.objects.create_user(username='souser', password='1234', first_name='teste', last_name='não manda', is_seller=True)
        cls.super_token = Token.objects.create(user=cls.super)
        cls.seller_token = Token.objects.create(user=cls.seller)
        cls.users = User.objects.all()
        cls.client: APIClient


    def test_seller_login(self):
        response = self.client.post('/api/login/', {"username": self.seller.username,"password": '1234'})
        expected_response = {"token": self.seller_token.key}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_login_wrong_credentials(self):
        response = self.client.post('/api/login/', {"username": self.seller.username,"password": '12345'})
        expected_response = {"detail": "invalid username or password"}
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), expected_response)

    def test_update_user_is_active_status_without_token(self):
        response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
        expected_response = {"detail": "Authentication credentials were not provided."}
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), expected_response)

    def test_update_user_is_active_status_with_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token 1' + self.super_token.key)
        response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
        expected_response = {"detail": "Invalid token."}
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), expected_response)


    def test_update_user_is_active_status_without_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
        response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
        expected_response = {"detail": "You do not have permission to perform this action."}
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), expected_response)


    # def test_update_user_is_active_status(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
    #     response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
    #     expected_response = {"is_active": False}
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), expected_response)

    # def test_update_user_without_permission(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
    #     response = self.client.patch('/api/accounts/2/', {"first_name": "Patch2", "last_name": "Teste"})
    #     expected_response = {"detail": "You do not have permission to perform this action."}
    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(response.json(), expected_response)

    # def test_update_user_is_active_status(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
    #     response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
    #     expected_response = {"is_active": False}
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), expected_response)
    
      # def test_list_all_users(self):
    #     response = self.client.get('/api/accounts/')
    #     self.assertEqual(response.status_code, 200)
    #     print(response.data)
    #     print(self.users)
    #     self.assertEqual(len(self.users), len(response.data))
    #     for user in self.users:
    #         self.assertIn(
    #             UserSerializer(instance=user).data,
    #             response.data
    #         )

    