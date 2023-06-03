# e-commerce-order-service-django

# Order Service APIs

Following are the steps to run this application:
1. Clone the repository
    - <code>git clone https://github.com/surojitdey/e-commerce-order-service-django.git</code>
2. Create python virtual environment and activate it(optional)
    - <code>python -m venv venv</code>
    - <code>source venv/bin/activate</code> (Linux/Mac)
    - <code>.\venv\Script\activate</code> (Windows)

3. Install the required dependencies
    - <code>pip install -r requirements.txt</code>

4. Migrate the database 
    - <code>python manage.py migrate</code> 

5. Run this application
    - <code>python manage.py runserver</code> 

6. Open <url>http://localhost:8000/swagger/</url> in browser to check the API endpoints

Following are the API endpoints:
1.  http://localhost:8000/order-service/orders/
  - Method: GET
  - Return a list of all orders with their details including nested items.
  - Authentication Token needed. <code>Authorization: Token <token></code>
2.  http://localhost:8000/order-service/orders/{id}
  - Method: GET
  - Retrieve a specific order by its ID. Response also include the nested items.
  - Authentication Token needed. <code>Authorization: Token <token></code>
3.  http://localhost:8000/order-service/orders/
  - Method: POST
  - Create a new order.
  - Body eg: {
      "status": "PENDING",
      "items": [
        {"name": "Item 1", "quantity": 2, "price": 10.0},
        {"name": "Item 2", "quantity": 1, "price": 15.0}
      ]
    }
  - Authentication Token needed. <code>Authorization: Token <token></code>
4.  http://localhost:8000/order-service/orders/{id}/update_status/
  - Method: PUT
  - Update status of an order.
  - Body eg: {
      "status": "SHIPPED"
    }
  - Authentication Token needed. <code>Authorization: Token <token></code>
5.  http://localhost:8000/v1/auth/login/username/
  - Method: POST
  - Login API for creting token for authentication and authorization.
  - Body data: { "username": <username>, "password": <password> }
  
> ***Note: Create a superuser before testing all the APIs. <code>python manage.py createsuperuser<code>
 
