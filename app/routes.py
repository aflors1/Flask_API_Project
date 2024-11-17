import logging
import time
import pandas as pd 
from datetime import datetime, timedelta
from flask import Flask, Blueprint, request, jsonify
from .data_generator import generate_products
import os
import psutil

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Blueprint('app',__name__)

# Initialize Flask 
# app = Flask(__name__)

# Track execution time for data generation
start_time = time.time()

def generate_and_save_data():

    # Path to the CSV file
    file_path = "products.csv"

    # Delete the file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
        logging.info(f"Existing file '{file_path}' deleted.")

    # Generate new data
    df = generate_products()
    
    # Track execution time for I/O 
    start_io_time = time.time()
    df.to_csv("products.csv", index=False)

    file_write_duration = time.time() - start_io_time
    file_size = os.path.getsize("products.csv") / (1024 * 1024)
    data_gen_duration = time.time() - start_time

    # Print log metrics 
    logging.info(f"Data generation took {data_gen_duration:.2f} seconds.")
    logging.info(f"File write took {file_write_duration:.2f} seconds.")
    logging.info(f"File size: {file_size:.2f} MB.")

generate_and_save_data() 

# Load CSV 
df = pd.read_csv("products.csv")
    
#### API ENDPOINTS ####

# a) Search by category 
@app.route('/filter_products', methods=['GET'])
def filter_products():

    # Reload the latest data from the CSV file
    df = pd.read_csv("products.csv")
    
    # Get query parameters 
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Category filter
    if category:
        filtered_products_df = df[df['category'] == category]
    else:
        filtered_products_df = df

    # Paginate results
    start = (page - 1) * per_page
    end = start + per_page
    paginated_products = filtered_products_df.iloc[start:end].to_dict(orient="records")

    # Return results in JSON format
    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": len(filtered_products_df),
        "total_pages": (len(filtered_products_df) + per_page - 1) // per_page,
        "products": paginated_products
    })
    
# b) Filter by price range
@app.route('/products/price', methods=['GET'])
def filter_by_price():

    # Reload the latest data from the CSV file
    df = pd.read_csv("products.csv")

    # Get query parameters
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', float('inf')))
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 100))

    # Filter products by price range
    filtered_products = df[(df['price'] >= min_price) & (df['price'] <= max_price)]

    # Paginate results
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = filtered_products.iloc[start_idx:end_idx] 

    # Return results in JSON format
    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": len(filtered_products),
        "total_pages": (len(filtered_products) + per_page - 1) // per_page,
        "products": paginated_products.to_dict(orient='records')  # Convert to JSON records
    })


# c) Count in-stock products 
@app.route('/products/in_stock', methods=['GET'])
def count_in_stock():

    # Reload the latest data from the CSV file
    df = pd.read_csv("products.csv")

    # Count in stock products
    count = df[df['in_stock'] == True].shape[0]

    # Return results in JSON format 
    return jsonify({"in_stock_count": count})

# d) Sort products 
@app.route('/products/sort', methods=['GET'])
def sort_products():

    # Reload the latest data from the CSV file
    df = pd.read_csv("products.csv")
    
    # Get query parameters
    sort_order = request.args.get('order', 'asc')
    ascending = True if sort_order == 'asc' else False
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # Sort data by price
    sorted_df = df.sort_values(by='price', ascending=ascending)
    total_sorted = len(sorted_df)

    # Paginate results
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = sorted_df.iloc[start:end] 

    # Convert DataFrame to dictionary for JSON response - more complex datafram here 
    products_dict = paginated_results.to_dict(orient='records')

    # Return results in JSON format 
    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total_sorted,
        "total_pages": (total_sorted + per_page - 1) // per_page,
        "products": products_dict
    })

    
# e) Top 10 recent products 
@app.route('/products/recent', methods=['GET'])
def top_recent_products():

    # Reload the latest data from the CSV file
    df = pd.read_csv("products.csv")

    # Sort by descending date added 
    recent_products = df.sort_values(by='date_added', ascending=False).head(10)
    results = recent_products.to_dict(orient='records')

    # Return results in JSON format 
    return jsonify(results)

#### Add new products 

def validate_product(product):

    # Validate product_name (must be a non-empty string)
    if 'product_name' not in product or not isinstance(product['product_name'], str) or not product['product_name'].strip():
        return "Invalid product_name: must be a non-empty string."
    
    # Define predefined categories for validation 
    categories = ["Electronics", "Clothing", "Books", "Home", "Baby", "Beauty", "Fitness", "Pet", "Holiday", "Kitchen"]

    # Validate category (must be a predefined category)
    if 'category' not in product or product['category'] not in categories:
        return f"Invalid category: must be one of {categories}."

    # Validate price (must be between 1 and 1000)
    if 'price' not in product or not isinstance(product['price'], float) or not (1 <= product['price'] <= 1000):
        return "Invalid price: must be between 1 and 1000."

    # Validate in_stock (must be a boolean)
    if 'in_stock' not in product or not isinstance(product['in_stock'], bool):
        return "Invalid in_stock: must be a boolean value (TRUE/FALSE)."

    # Validate date_added (must be a date within the last year)
    if 'date_added' not in product:
        return "Missing date_added."
    
    try:
        date_added = datetime.strptime(product['date_added'], "%Y-%m-%d")
        if date_added < datetime.now() - timedelta(days=365):
            return "Invalid date_added: must be within the last year."
    except ValueError:
        return "Invalid date_added: must be in the format YYYY-MM-DD."

    return None  # No errors, all validations passed

@app.route('/products', methods=['POST'])
def add_product():
    
    global df  

    try:
        # Load the CSV file to get current products 
        df = pd.read_csv("products.csv")
        
        # Get data from POSTMAN request
        data = request.get_json()

        # Validate the product meets requirements
        validation_error = validate_product(data)
        if validation_error:
            return jsonify({"error": validation_error}), 400

        # Create a new product as a DataFrame
        new_product = pd.DataFrame([{
            "product_id": len(df)+1,
            "product_name": data['product_name'],
            "category": data['category'],
            "price": data['price'],
            "in_stock": data['in_stock'],
            "date_added": data['date_added']
        }])

        # Concatenate the new product DataFrame with the existing DataFrame
        df = pd.concat([df, new_product], ignore_index=True)

        # Save the updated DataFrame to CSV
        df.to_csv("products.csv", index=False)

        # Return a success response with the new product data
        return jsonify({"message": "Product added successfully", "product": new_product.to_dict(orient='records')[0]}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the app
# if __name__ == '__main__':
    #generate_and_save_data() 
    # app.run(debug=True, use_reloader=False)