## **Flask API Project**

### **Overview**
This project is a Flask-based API for managing product data. It supports endpoints for filtering, sorting, and adding products, as well as retrieving recent products and counting in-stock items. The product data is generated and saved as a CSV file.

---

### **Features**
- **Filter Products by Category:** Filter products based on their category with pagination.
- **Filter by Price Range:** Retrieve products within a specified price range.
- **Sort Products by Price:** Sort products in ascending or descending order with pagination.
- **Count In-Stock Products:** Get the count of products currently in stock.
- **Retrieve Recent Products:** Get the 10 most recently added products.
- **Add New Products:** Add a new product to the dataset after validation.

---

### **Setup Instructions**

#### **Prerequisites**
- Python 3.9+ installed
- `pip` for managing Python packages
- Recommended: Virtual environment (`venv`) for isolating dependencies

#### **Installation**
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-folder>
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Start the Flask application to access the API in Postman or the browser:
    ```bash
    python -m app
The app will run on http://127.0.0.1:5000.

### **Available API Endpoints**
#### **1. Filter Products by Category**
URL: /filter_products

Method: GET

Query Parameters:
* category: (optional) Filter products by category.
* page: (optional) Page number (default is 1).
* per_page: (optional) Number of products per page (default is 10).
Example:

```bash
GET http://127.0.0.1:5000/filter_products?category=Electronics&page=1&per_page=5
```
#### **2. Filter Products by Price** 
URL: /products/price

Method: GET

Query Parameters:

* min_price: Minimum price (default is 0).
* max_price: Maximum price (default is unlimited).
* page: Page number (default is 1).
* per_page: Number of products per page (default is 100).
Example:

```bash
GET http://127.0.0.1:5000/products/price?min_price=10&max_price=100&page=1&per_page=5
```
#### **3. Count In-Stock Products**
URL: /products/in_stock

Method: GET

Example:
```bash
GET http://127.0.0.1:5000/products/in_stock
```
#### **4. Sort Products by Price** 
URL: /products/sort

Method: GET

Query Parameters:
* order: Sorting order (asc for ascending or desc for descending).
* page: Page number (default is 1).
* per_page: Number of products per page (default is 5).
Example:
```bash
GET http://127.0.0.1:5000/products/sort?order=desc&page=1&per_page=3
```
#### **5. Retrieve Recent Products**
URL: /products/recent

Method: GET

Example:
```bash
GET http://127.0.0.1:5000/products/recent
```
### **6. Add a New Product**
URL: /products

Method: POST

Body: The following fields are required:

* product_name: Name of the product (string).
* category: Category of the product (must be predefined, e.g., "Electronics").
* price: Price of the product (float between 1 and 1000).
* in_stock: Boolean indicating if the product is in stock.
* date_added: Date when the product was added (YYYY-MM-DD format, within the last year).

Example:
```bash
POST http://127.0.0.1:5000/products
Content-Type: application/json
{
  "product_name": "Smartphone",
  "category": "Electronics",
  "price": 699.99,
  "in_stock": true,
  "date_added": "2024-11-10"
} 
```

### **Testing**
#### **Running Unit Tests**
Run the unit tests to ensure all endpoints function correctly:

```bash
pytest
```
### **Logging**
Logs are generated to track data generation progress and API usage. They include metrics like:

* Data generation time
* File writing time
* File size

Logs are output to the console for debugging purposes.

### **Directory Structure**
```bash
flask_api_project/
│
├── app/
│   ├── __init__.py            # Testing app setup
│   ├── __main__.py            # Flask app setup
│   ├── routes.py              # API routes and logic
│   ├── data_generator.py      # Product data generation logic
│
├── test/
│   ├── test_routes.py         # Unit tests for API endpoints
│   ├── test_data_generator.py # Unit tests for data generator function
│
├── README.md          # Project documentation
├── requirements.txt   # Project documentation
└── products.csv       # Generated product data
```

### **Future Improvements**
1. Increase the speed of def generate_products() 
This program usually averages 80-90 seconds to generate one million rows. I think this could be optimized more to reach closer to one minute. 

2. Table to track logs for runtime
I'd like to output the logs for each run with a timestamp, file size, and time it took to generate data into a CSV for better performance tracking. 

3. Adidtional unit test 
The API endpoint needs (at least) one more unit test for posting a bad record and confirming that an error code is given rather than a success code if the entry doesn't meet specifications. 

4. More flexibility with Top Recent Products API
It would be nice to give more flexibility with this one to show a different number of top products rather than always just the top 10 because there are most likely more than 10 products with the same, latest added date. 