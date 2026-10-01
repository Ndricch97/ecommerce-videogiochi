# Video Game E-commerce Database

Academic project focused on the design and management of a relational database for a video game e-commerce system.

The application is written in **Python** and uses **SQLAlchemy ORM** to model and interact with a **MySQL** database. It provides the main entities and CRUD operations needed to manage customers, products, orders, reviews, wishlists, administrators, and inventory.

## Project goals

The project was developed to apply relational database concepts in a practical scenario, including:

- relational data modelling;
- primary and foreign keys;
- one-to-many and many-to-many relationships;
- association tables;
- CRUD operations;
- data constraints and validation;
- database interaction through an ORM.

## Technologies

- **Python**
- **MySQL**
- **SQLAlchemy**
- **MySQL Connector/Python**

## Data model

The database contains the following main entities:

- **Cliente** — customer information and account data
- **Amministratore** — administrator information
- **Magazzino** — inventory quantities
- **Prodotto** — video game catalogue
- **Ordine** — customer orders
- **Recensione** — product reviews
- **Wishlist** — customer wishlists
- **Ordine_Prodotto** — association between orders and products
- **Wishlist_Prodotto** — association between wishlists and products

The association tables are used to model many-to-many relationships between orders/products and wishlists/products.

## Implemented features

### Create

The application includes functions to:

- create customers and administrators;
- add products;
- create orders;
- add product reviews;
- create a wishlist for a customer;
- add products to orders and wishlists.

### Read

Available queries include:

- listing customers and administrators;
- viewing products in inventory;
- viewing a single product;
- retrieving a customer's order history;
- retrieving reviews for a product;
- listing products contained in an order or wishlist.

### Update

The project supports updates to:

- customer data;
- administrator data;
- product information;
- inventory quantities;
- order status.

### Delete

The application includes operations to:

- delete customers and administrators;
- delete products, orders, reviews, and wishlists;
- remove products from orders and wishlists.

## Project structure

```text
ecommerce-videogiochi/
├── main.py
└── README.md
```

The current implementation is contained in `main.py`, which defines the SQLAlchemy models, database relationships, and CRUD functions.

## Author

**Andrea Marrocco**
