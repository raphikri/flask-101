# tests/test_views.py
from flask_testing import TestCase
from wsgi import app, PRODUCTS, IDENTIFIER_GENERATOR
import itertools

class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_products_json(self):
        response = self.client.get("/api/v1/products")
        products = response.json
        self.assertIsInstance(products, dict)
        self.assertEqual(len(products), len(PRODUCTS)) # 2 is not a mistake here.

    def test_product_json(self):
        response = self.client.get("/api/v1/products/1")
        product = response.json
        status_code = response.status_code
        self.assertIsInstance(product, dict)
        self.assertEqual(product, PRODUCTS[1])
        self.assertEqual(status_code, 200)

    def test_product_invalid_id_json(self):
        response = self.client.get("/api/v1/products/100")
        status_code = response.status_code
        self.assertEqual(status_code, 404)

    def test_delete_product_json(self):
        response = self.client.delete("/api/v1/products/2")
        status_code = response.status_code
        self.assertEqual(status_code, 204)

    def test_delete_invalid_product_json(self):
        response = self.client.delete("/api/v1/products/5")
        status_code = response.status_code
        self.assertEqual(status_code, 204)

    def test_post_product_json(self):
        response = self.client.post("/api/v1/products", json={ 'name': 'Raph'})
        START_INDEX = len(PRODUCTS) + 1
        IDENTIFIER_GENERATOR = itertools.count(START_INDEX)
        next_value = next(IDENTIFIER_GENERATOR)
        status_code = response.status_code
        self.assertEqual(status_code, 201)
        self.assertEqual(PRODUCTS[next_value], {'id': next_value, 'name': 'Raph'})

    def test_put_product_json(self):
        response = self.client.put("/api/v1/products/1", json={ 'name': 'Raph'})
        status_code = response.status_code
        self.assertEqual(status_code, 204)
        self.assertEqual(PRODUCTS[1], {'id': 1, 'name': 'Raph'})
