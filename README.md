# Telus TakeOut
This is a food ordering service web application.  It is based on the open
source seed project generated by
**[AppSeed](https://appseed.us/generator/material-kit/)** using the Flask
Framework and Material Kit design.  It explores Flask features to build
an application that includes authentication and an underlying database.

## Features
- Database: SQLite
- DB Tools: SQLAlchemy ORM, Flask-Migrate (schema migrations)
- Session-based authentication (via flask_login)
- Forms validation

## Requirements
The primary objective of this app is to create a takeout ordering system
for pizzas and subs (sandwiches).

1. When ordering takeout, users must specify:
    - Who they are --> their name and phone number
    - When they want to receive their order --> date and time
    - How they want to receive their order --> delivery or pickup
    - What they want to order --> pizza or sub

1. If users choose delivery, they must provide a delivery address.

1. If users order pizza, they may select up to 3 toppings from the following
   list:
    - Pepperoni
    - Mushrooms
    - BlackOlives
    - Pineapple

1. If users order sandwiches, they may select up to 3 toppings from the
   following list:
        Lettuce
        Tomato
        BlackOlives
        Pineapple

1. Employees must be able to access a list of orders.  This list must:
    - Include customer details (e.g., username, phone number, requested
      delivery date/time).
    - Be sortable by at least desired delivery dates/times.
    - Link to additional order details.

## Getting Started
### Using `Windows` and `PowerShell`

<br />

> Set Up the Python Virtual Environment

```bash
# Create the Python virtual environment.
$ python -m venv .venv

# Activate the virtual environment.
$ .\.venv\Scripts\Activate.ps1

# Upgrade Pip and Wheel.
$ python -m pip install --upgrade pip wheel

# Install the required modules:
pip install -r .\requirements.txt
```

> Set Up Flask Environment (for Development Purposes)

```bash
$ # Powershell
$ $env:DEBUG=$true
$ $env:FLASK_APP = ".\run.py"
$ $env:FLASK_ENV = "development"
```

> Start the App

```bash
$ flask run
```

Navigate to `http://127.0.0.1:5000/` in your browser to use the web application.

### Using the App (Creating Users)
By default, the app redirects guest users to authenticate.  In order to access
the private pages, follow this set up:

- Start the app via `flask run`
- Access the `signup` page and create a new user:
  - `http://127.0.0.1:5000/signup`
- Access the `login` page and authenticate
  - `http://127.0.0.1:5000/login`

## Code Structure
This application is organized as shown below:

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |
   |    |-- home/                           # A simple app that serve HTML files
   |    |    |-- routes.py                  # Defined app routes
   |    |
   |    |-- authentication/                 # Handles auth routes (login and signup)
   |    |    |-- routes.py                  # Defines authentication routes
   |    |    |-- models.py                  # Defines models
   |    |    |-- forms.py                   # Define auth forms (login and signup)
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>          # CSS files, JavaScript files
   |    |
   |    |-- templates/                      # Templates used to render pages
   |    |    |-- includes/                  # HTML chunks and components
   |    |    |    |-- navigation.html       # Top menu component
   |    |    |    |-- sidebar.html          # Sidebar component
   |    |    |    |-- footer.html           # App Footer
   |    |    |    |-- scripts.html          # Scripts common to all pages
   |    |    |
   |    |    |-- layouts/                   # Master pages
   |    |    |    |-- base-fullscreen.html  # Used by Authentication pages
   |    |    |    |-- base.html             # Used by common pages
   |    |    |
   |    |    |-- accounts/                  # Authentication pages
   |    |    |    |-- login.html            # Login page
   |    |    |    |-- register.html         # Register page
   |    |    |
   |    |    |-- home/                      # UI Kit Pages
   |    |         |-- index.html            # Index page
   |    |         |-- 404-page.html         # 404 page
   |    |         |-- *.html                # All other pages
   |    |
   |  config.py                             # Set up the app
   |    __init__.py                         # Initialize the app
   |
   |-- requirements.txt                     # App Dependencies
   |
   |-- .env.ps1                             # Inject Configuration via env vars
   |-- run.py                               # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```
## Database Schema
The underlying app data is organized in a relational database as follows:

```bash
users: {
  id: int        -> primary key
  username: str  -> unique
  email: str     -> unique
  password: binary
  telephone: str
  address: str
  is_employee: bool
}

orders: {
  id: int                 # Primary key
  username: str           # Foreign key
  delivery_method: str    # [Pickup|Delivery]
  delivery_address: str   # If delivery_method = Delivery
  contact_phone: str
  ordered_at: datetime
  requested_for: datetime # When the customer wants the order
  status: str             # [Ordered|Complete|Canceled|Abandoned]
}

order_details: {
  id: int                 # Primary key
  order_id: int           # Foreign key
  item: str
  topping_1: str          #-|
  topping_2: str          # |-> may be store as JSON blob for future growth
  topping_3: str          #-|
  quantity: int
  cost: float
}

```