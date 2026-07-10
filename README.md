# Computer Shop
#### Video Demo:  https://youtu.be/RhQi9tO6t0c
#### Author: BrandenZsiros
#### Description: A simple web app to simulate an potential online store for a business.

## Table of contents
1. [Learning Objectives](#learning-objective)
2. [Technology](#technology)
3. [Design](#design)
4. [Files](#files)
5. [Future improvements](#future-improvements)
6. [Contributing](#contributing)
7. [Licence](#licence)

## Learning Objective
Construct a web app experimenting with server-side rendering to understand the trade-off between using APIs for transferring data to the frontend for client side rendering vs rendering the UI server-side. To better understand the trade-off that is being made design wise due to the common understanding that APIs require you to manage more components.

For similar reasons I would also like the experiment with a Controller - View model compared to the common Model - View - Controller design. To help get a better idea on the reason behind abstracting out the data retrieval and business rule enforcement details from the controller.

Construct a mobile-friendly and widescreen-friendly UI to assist in understanding what design traits would be needed to meet booth requirements since wide screen is neglected by most sites.

## Technology
- Flask - Python based web framework for handling http requests and routing has Jinja as default templating language making it useful for server-side rendering.
- Jinja - templating engine for creating dynamic content the core for server-side rendering.
- SQLite3 - A small lightweight database focused on a single file doesn't scale much making it useful for smaller applications like this
- Bootstrap - CSS framework for designing for responsive design and is mobile friendly

## Design
When designing the system 2 main actors occurred being the consumer and staff from which responsibilities consisted of using the site to purchase goods and updating the site to reflect the real state of the business for more detail see [Use Case Diagram](./docs/diagrams/UseCase.svg)

Based on this since we have understand the use cases we want to implement we can now construct a UI surrounding notably we need to implement access controls to prevent the consumer actor from using the Staffs use cases so the site needs to be divided to 2 parts based on whether the user is logged in or not and since the employee needs has many use cases we developed a portal to centrally manage flow. For the full initial design see [Storyboard](./docs/diagrams/Storyboard.svg)

Now based on this we now know the types on data that needs to be stored in particular we can identify that we need records to manage users, store the orders that have been places, and store the details of all the products and construct a one-to-many relationship between the products in the system and the orders that contain it. For the schema see [Entity Relationship Diagram](./docs/diagrams/ERDiagram.md)

## Files
- app.py - The controller for the project.
- shop.db - The database used for the project.
- requirements.txt - The imports used fort the project.
- styles.css - Common styles used across the site.
- I_heart_validator.png - Asset used to show the site has valid html.
- favicon.ico - The favicon for the site.
- layout.html - Common template that all other pages derive from includes top bar.
- home.html - The home page template that displays all products.
- product.html - The view template for the details of the product.
- buy.html - Form template for filling out the data needed for purchasing a product.
- success.html - Confirmation template that an action has been successful.
- login.html - The template for employees to log into the site.
- portal.html - The home page template for employees to manage the site.
- restock.html - Template form for restocking a given product.
- stock.html - Template for viewing the inventory of the entire store.
- add.html - Template for adding a new product to the system.
- remove.html - Template for removing a given product from the store.
- orders.html - Template for viewing a fulfilling all the orders placed.
- register.html - A debug template for filling out a new user since password hashing is used.

## Future improvements
- Add a cart system that allows ordering multiple products in a order.
- Use an external provider to handle identity management.
- Redesign the home page to include a hero image (Large image banner) to improve design.
- Modify the cards to contain images of the product and store images in blob storage in the database.
- Implement a system to allow customers to log in saving their purchases information for quicker use case flow.
- Implement infinite scrolling to improve the sites scalability by not loading all the products on the home screen.
- Allow a dropdown menu of products to easily remove products.

## Contributing
I'm not accepting contributions at this time since this was designed to be a small project for learning and not actively maintaining it. Feel free to fork it and add to it if you feel the need to.

## Licence
[MIT](https://choosealicense.com/licenses/mit/)
