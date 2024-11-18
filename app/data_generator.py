from faker import Faker
import pandas as pd
import numpy as np

# Initialize Faker(), predefined categories, and dates 
fake = Faker()
categories = ["Electronics", "Clothing", "Books", "Home", "Baby", "Beauty", "Fitness", "Pet", "Holiday", "Kitchen"]
start_date = np.datetime64("today") 
end_date = start_date + np.timedelta64(365, "D")

# Generate data to meet specifications
def generate_products(n=1000000):
    
    # Unique product ID 
    product_ids = np.arange(1, n + 1)

    # Random word 
    product_names = [fake.word().capitalize() for _ in range(n)]

    # Random predefined category 
    product_categories = np.random.choice(categories, size=n)

    # Random price between 1 and 1000
    prices = np.round(np.random.uniform(1, 1000, n), 2)

    # Random boolean - added weights for true/false 
    in_stock_status = np.random.choice([True, False], size=n, p=[0.85, 0.15])

    # Random dates within the last year
    dates_added = np.random.randint(start_date.astype("int64"), end_date.astype("int64"), n).astype("datetime64[D]")
    dates_added_formatted = dates_added.astype(str)
    
    df = pd.DataFrame({
        "product_id": product_ids,
        "product_name": product_names,
        "category": product_categories,
        "price": prices,
        "in_stock": in_stock_status,
        "date_added": dates_added_formatted 
    })

    return df
