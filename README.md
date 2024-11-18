## **Flask API Project**

### **Overview**

This project is a Flask-based API for managing product data. It supports endpoints for filtering, sorting, adding products, retrieving recent products, and counting in-stock items. The product data is generated and saved as a CSV file with one million rows and 6 columns. 

---

### **Features**

- **Filter Products by Category:** Filter products based on their category with pagination.
- **Filter by Price Range:** Retrieve products within a specified price range with pagination.
- **Sort Products by Price:** Sort products in ascending or descending order with pagination.
- **Count In-Stock Products:** Get the count of products currently in stock.
- **Retrieve Recent Products:** Get the 10 most recently added products by added_date. 
- **Add New Products:** Add a new product to the dataset after validation that it meets specifications. 

---

### **Setup Instructions**

#### **Prerequisites**

- Python 3.9+ installed
- `pip` for managing Python packages

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
    python -m app.run

The app will run on http://127.0.0.1:5000.

### **Generate Data**

The function def generate_products() creates a data table and saves it as "products.csv". It is set to create one million rows. 

   | Column | Type | Description |
   | ------ | ---- | ----------- |
   | product_id | Integer | Unique identifier | 
   | product_name | String | Randomly generated name | 
   | category | String | Predefined list: ["Electronics", "Clothing", "Books", "Home", "Baby", "Beauty", "Fitness", "Pet", "Holiday", "Kitchen"]
   | price | Float | Between 1 and 1000 | 
   | in_stock | Boolean | True/False | 
   | date_added | String | Randomly generated within the last year 

### **Available API Endpoints**

#### **1. Filter Products by Category**

URL: /filter_products

Method: GET

Query Parameters:

* category: Filter products by category.
* page: (optional) Page number (default is 1).
* per_page: (optional) Number of products per page (default is 10).

Example:

```bash
GET http://127.0.0.1:5000/filter_products?category=Clothing&page=1&per_page=5
```
#### **2. Filter Products by Price** 

URL: /products/price

Method: GET

Query Parameters:

* min_price: Minimum price 
* max_price: Maximum price 
* page: Page number (default is 1).
* per_page: Number of products per page (default is 10).

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
* per_page: Number of products per page (default is 10).

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

Method: POST - use Postman or other developer tool 

Body: The following fields are required:

* product_name: Name of the product (string).
* category: Category of the product (must be predefined).
* - categories = ["Electronics", "Clothing", "Books", "Home", "Baby", "Beauty", "Fitness", "Pet", "Holiday", "Kitchen"] 
* price: Price of the product (float between 1 and 1000).
* in_stock: Boolean indicating if the product is in stock.
* date_added: Date when the product was added (YYYY-MM-DD format, within the last year of the date you run the code).

Example:

```bash
POST http://127.0.0.1:5000/products

Content-Type: application/json
{
  "product_name": "T-shirt",
  "category": "Clothing",
  "price": 19.99,
  "in_stock": true,
  "date_added": "2024-11-10"
} 
```

### **Testing**

#### **Running Unit Tests**

Run the unit tests to ensure all endpoints function correctly:

```bash
pytest

# to run separately 
pytest test/test_routes.py 
pytest test/test_data_generator.py 
```
### **Logging**

Logs are generated to track data generation progress. Metrics include:

* Data generation time
* I/O file writing time
* File size

Logs are output to the console for debugging purposes.

### **Directory Structure**

```bash
flask_api_project/
│
├── app/
│   ├── __init__.py            # Testing app setup
│   ├── run.py                 # Run Flask API 
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

1. Product names that make sense 

   Right now the product names are random words so they may not be nouns much less nouns that make sense for their category. Checking to make sure they were nouns drastically slowed down the program. In this case, speed was prioritized as the names themselves were not as important in getting the API functioning.  

2. Table to track logs for runtime 

   Create a control table of runs to output the timestamp, file size, and time it took to generate data into a CSV for better performance tracking. 

3. Additional unit test 

   The API endpoint needs (at least) one more unit test for posting a bad record and confirming that an error code is given rather than a success code if the entry doesn't meet specifications. 

4. More flexibility with Top Recent Products API

   More flexibility with this one to show a different number of top products rather than always just the top 10 because there are most likely more than 10 products with the same, latest added date. Additional levels of sorting would also be helpful here so it could sort on date_added and price for example. 