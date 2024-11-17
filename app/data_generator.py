import random
import string
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd
import numpy as np

# Initialize Faker() and predefined categories 
fake = Faker()
categories = ["Electronics", "Clothing", "Books", "Home", "Baby", "Beauty", "Fitness", "Pet", "Holiday", "Kitchen"]

def generate_products(n=1000000):
    # Generate data to meet specifications
    product_ids = np.arange(1, n + 1)
    product_names = [fake.word().capitalize() for _ in range(n)]
    product_categories = np.random.choice(categories, size=n)
    prices = np.round(np.random.uniform(1, 1000, n), 2)
    in_stock_status = np.random.choice([True, False], size=n, p=[0.85, 0.15])
    dates_added = [fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d") for _ in range(n)]
    
    df = pd.DataFrame({
        "product_id": product_ids,
        "product_name": product_names,
        "category": product_categories,
        "price": prices,
        "in_stock": in_stock_status,
        "date_added": dates_added
    })

    return df
