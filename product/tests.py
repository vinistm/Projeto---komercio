from urllib import response
from django.test import TestCase
from product.models import Product
from users.models import User
from product.serializers import ListProductSerializer
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase,APIClient
from rest_framework.views import Response, status

class ProductModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        
        cls.seller_username = "teste"
        cls.seller_password = "1234"
        cls.seller_first_name = "Teste"
        cls.seller_last_name = "Testado"
        cls.seller_is_seller = True

        cls.seller = User.objects.create_user(username=cls.seller_username, password=cls.seller_password, first_name=cls.seller_first_name, last_name=cls.seller_last_name, is_seller=cls.seller_is_seller)

        cls.description = "Smartband XYZ 3.0"
        cls.price = 100.99
        cls.quantity = 15

        cls.product = Product.objects.create(description=cls.description, price=cls.price, quantity=cls.quantity, seller=cls.seller)

    def test_product_has_information_fields(self):            
        self.assertEqual(self.product.description, self.description)
        self.assertEqual(self.product.price, self.price)
        self.assertEqual(self.product.quantity, self.quantity)
        self.assertEqual(self.product.seller, self.seller)


class ProductsViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seller = User.objects.create_user(username='testee', password='12345', first_name='teste', last_name='da Testado', is_seller=True)
        cls.super = User.objects.create_superuser(username='superteste', password='12345', first_name='super', last_name='da Testado')
        cls.seller_token = Token.objects.create(user=cls.seller)
        cls.super_token = Token.objects.create(user=cls.super)
        cls.products = [Product.objects.create(description=f'Product {product_id}', price=100.00, quantity=15, seller=cls.seller) for product_id in range(1, 6)]
        cls.products2 = [Product.objects.create(description=f'Product {product_id}', price=100.00, quantity=10, seller=cls.seller) for product_id in range(1, 6)]
        cls.client: APIClient
        cls.base_url = '/api/products/'

    def test_can_retrieve_a_specific_product(self):
        product = self.products[0]
        response = self.client.get(f'/api/products/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['description'], product.description)

        self.assertEqual(
            ListProductSerializer(instance=product).data,
            response.data
        )


    def test_create_product_without_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
        product_info = {"description": "Smartband XYZ 3.0",
                        "price": 100.99,
                        "quantity": 15}
        response = self.client.post('/api/products/', product_info)
        expected_response = {"detail": "You do not have permission to perform this action."}
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), expected_response)


    def test_create_product_without_required_fields(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
        product_info = {"description": "Smartband XYZ 3.0",
                        "price": 100.99}
        response = self.client.post('/api/products/', product_info)
        expected_response = {"quantity": ["This field is required."]}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), expected_response)

    # def test_create_product(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
    #     product_info = {"description": "Smartband XYZ 3.0",
    #                     "price": 100.99,
    #                     "quantity": 15}
    #     response = self.client.post('/api/products/', product_info)
    #     seller_response = response.json()['seller']
    #     expected_response = {"id": self.products[-1].id + 1,
    #                         "description": product_info['description'],
    #                         "price": product_info['price'],
    #                         "quantity": product_info['quantity'],
    #                         "is_active": False,
    #                         "seller": {
    #                             "id": self.seller.id,
    #                             "username": self.seller.username,
    #                             "first_name": self.seller.first_name,
    #                             "last_name": self.seller.last_name,
    #                             "is_seller": self.seller.is_seller
    #                         }}
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(response.json(), expected_response)

    # def test_update_product_without_permission(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
    #     product_info = {"price": 5.99}
    #     response = self.client.patch('/api/products/1/', product_info)
    #     expected_response = {"detail": "You do not have permission to perform this action."}
    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(response.json(), expected_response)

    # def test_update_product(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
    #     product = self.products[0]
    #     product_info = {"price": 5.99}
    #     response = self.client.patch('/api/products/1/', product_info)
    #     seller_response = response.json()['seller']
    #     expected_response = {"id": product.id,
    #                         "description": product.description,
    #                         "price": product_info['price'],
    #                         "quantity": product.quantity,
    #                         "is_active": True,
    #                         "seller": {
    #                             "id": self.seller.id,
    #                             "username": self.seller.username,
    #                             "first_name": self.seller.first_name,
    #                             "last_name": self.seller.last_name,
    #                             "is_seller": self.seller.is_seller,

    #                         }}
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), expected_response)



    # def test_can_list_all_products(self):
    #     response = self.client.get('/api/products/')
    #     self.assertEqual(response.status_code, 200)
      
    #     self.assertEqual(len(self.products), len(response.data))

    #     for product in self.products:
    #         self.assertIn(
    #             ListProductSerializer(instance=product).data,
    #             response.data
    #         )

    # def test_create_product_with_negative_quantity(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
    #     product_info = {"description": "Smartband XYZ 3.0",
    #                     "price": 100.99,
    #                     "quantity": -15}
    #     response = self.client.post('/api/products/', product_info)
    #     expected_response = {"quantity": ["Ensure this value is greater than or equal to 0."]}
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json(), expected_response)
    