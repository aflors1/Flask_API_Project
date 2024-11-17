import unittest
from app import create_app  # Import create_app to initialize the app

class TestFlaskAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True  # Ensure testing mode is enabled

    def test_add_product(self):
        response = self.app.post('/products', json={
            'product_name': 'Test Product',
            'category': 'Clothing',
            'price': 99.99,
            'in_stock': True,
            'date_added': '2024-11-15'
        })
        self.assertEqual(response.status_code, 201)  # Expecting a 201 Created response

    def test_count_in_stock(self):
        response = self.app.get('/products/in_stock')
        self.assertEqual(response.status_code, 200)  # Expecting a 200 OK response

    def test_filter_by_price(self):
        response = self.app.get('/products/price', query_string={'min_price': 10, 'max_price': 100})
        self.assertEqual(response.status_code, 200)

    def test_filter_products(self):
        response = self.app.get('/filter_products', query_string={'category': 'Electronics'})
        self.assertEqual(response.status_code, 200)

    def test_sort_products(self):
        response = self.app.get('/products/sort', query_string={'order': 'asc'})
        self.assertEqual(response.status_code, 200)

    def test_top_recent_products(self):
        response = self.app.get('/products/recent')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
