import unittest
import pandas as pd
import numpy as np
from app.data_generator import generate_products   

class TestDataGenerator(unittest.TestCase):

    def test_empty_dataset(self):
        # Test for generating an empty dataset
        result = generate_products(0)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 0)

    def test_large_dataset(self):
        # Test for generating a large dataset - handles at least a million rows
        result = generate_products(1005000)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1005000)

    def test_invalid_input(self):
        # Test for invalid input
        with self.assertRaises(TypeError):
            generate_products("string")  # Pass a string instead of an integer
        with self.assertRaises(ValueError):
            generate_products(-10)  # Pass a negative number

    def test_column_names(self):
        # Test that product.csv has the correct column names
        result = generate_products(100)
        expected_columns = ["product_id", "product_name", "category", "price", "in_stock", "date_added"]
        self.assertTrue(all(col in result.columns for col in expected_columns))

    def test_product_ids(self):
        # Test that the product IDs are unique
        result = generate_products(100)
        self.assertTrue(result['product_id'].is_unique) 

    def test_price_range(self):
        # Test that the prices are within 1 to 1000
        result = generate_products(100)
        self.assertTrue((result['price'] >= 1).all())  
        self.assertTrue((result['price'] <= 1000).all())  

    def test_in_stock_status_distribution(self):
        # Test the in_stock status distribution
        result = generate_products(1000)
        in_stock_count = result['in_stock'].sum()
        out_of_stock_count = len(result) - in_stock_count
        # Since the probability is weighted 0.85 for in_stock and 0.15 for out_of_stock, check for a reasonable range
        self.assertTrue(0.8 <= in_stock_count / len(result) <= 0.9)
        self.assertTrue(0.1 <= out_of_stock_count / len(result) <= 0.2)

    def test_dates_within_last_year(self):
        #Test valid date range 
        result = generate_products(1000) 
        current_date = np.datetime64('today', 'D')
        one_year_ago = current_date - np.timedelta64(365, 'D')
        
        # Convert 'date_added' to match the format of generated dates
        dates = np.array(pd.to_datetime(result['date_added']).dt.date, dtype='datetime64[D]')  
        
        # Ensure that all dates are within the last year
        self.assertTrue(dates.min() >= one_year_ago)  
        self.assertTrue(dates.max() <= current_date)  

if __name__ == "__main__":
    unittest.main()