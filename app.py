import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///shop.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    # Display all products in home page
    products = db.execute("SELECT productID, name, category, salePrice FROM Product")
    return render_template("home.html", products=products)


@app.route("/view/<id>")
def view(id):
    # Show more detail related to an item
    item = db.execute(
        "SELECT productID, name, category, salePrice, description FROM Product WHERE productID = ?", id)
    if len(item) == 0:
        return apology("Item ID does not exist")
    return render_template("product.html", item=item)


@app.route("/buy/<id>", methods=["GET", "POST"])
def buy(id):
    if request.method == "POST":
        # Retrive form fields
        name = request.form.get("name")
        address = request.form.get("address")
        cardNumber = request.form.get("cardNumber")
        CCV = request.form.get("CCV")
        expiry = request.form.get("expiry")
        # Check for empty fields
        if not name:
            return apology("must provide name", 400)
        if not address:
            return apology("must provide address", 400)
        if not cardNumber:
            return apology("must provide card Number", 400)
        if not CCV:
            return apology("must provide CCV", 400)
        if not expiry:
            return apology("must provide Expiry", 400)
        # Insert details into db and confirm success
        db.execute("INSERT INTO Orders VALUES (NULL, ?, ?, DATE('NOW'), ?, ?, ?, ?, 0)",
                   id, name, address, cardNumber, CCV, expiry)

        return render_template("success.html", id=id)
    else:
        # Send user to form page
        return render_template("buy.html", id=id)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/portal")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/portal")
@login_required
def portal():
    # Send user to the portal page
    return render_template("/portal.html")


@app.route("/restock", methods=["GET", "POST"])
@login_required
def restock():
    if request.method == "POST":
        # Get form fields
        productID = request.form.get("productID")
        # Make sure form fields arnt empty
        if not productID:
            return apology("Must provide productID", 400)
        # increment stock and get the restock url
        db.execute("UPDATE Product SET instock = instock + 1 WHERE productID = ?", productID)
        URL = db.execute("SELECT restockURL FROM Product WHERE productID = ?", productID)
        # Send user to the URL to restock
        return redirect(URL[0]["restockURL"])
    else:
        # Show all products and give option to restock
        products = db.execute("SELECT productID, name, instock, restockPrice FROM Product")
        return render_template("/restock.html", products=products)


@app.route("/stock")
@login_required
def stock():
    # Get all products
    products = db.execute("SELECT name, instock, restockPrice, salePrice FROM Product")
    # maintain new array that contains profit per unit
    profitPerUnit = []
    for i in range(len(products)):
        profitPerUnit.append(products[i]["salePrice"] - products[i]["restockPrice"])
    # Display the products with there profit per unit
    return render_template("/stock.html", profitPerUnit=profitPerUnit, products=products)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        # Retrieve form fields
        name = request.form.get("name")
        category = request.form.get("category")
        description = request.form.get("description")
        salePrice = request.form.get("salePrice")
        restockPrice = request.form.get("restockPrice")
        restockURL = request.form.get("restockURL")
        instock = request.form.get("inStock")
        # Validate the form fields to ensure they are filled and of correct type
        if not name:
            return apology("must provide name", 400)
        if not category:
            return apology("must provide category", 400)
        if not description:
            return apology("must provide description", 400)
        if not salePrice or not salePrice.replace(".", "", 1).isdigit():
            return apology("must provide valid sale Price", 400)
        if not restockPrice or not restockPrice.replace(".", "", 1).isdigit():
            return apology("must provide valid restockPrice", 400)
        if not restockURL:
            return apology("must provide Url for restocking", 400)
        if not instock:
            return apology("must provide innital stock quanity", 400)
        try:
            # Insert into the db
            db.execute("INSERT INTO product VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", name,
                       category, description, instock, restockPrice, salePrice, restockURL)
        except ValueError:
            return apology("inncorrect type", 400)
        # Send user back
        return render_template("/portal.html")
    else:
        # Provide the form to fill out to add a product
        return render_template("/add.html")


@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    if request.method == "POST":
        # Get form fields
        name = request.form.get("name")
        if not name:
            return apology("must provide product name", 400)
        # Run a check to ensure it exists
        matches = db.execute("SELECT * FROM Product WHERE name = ?", name)
        if len(matches) < 1:
            return apology("Cannot find product")
        try:
            # Delete it's orders then remove it
            db.execute(
                "DELETE FROM Orders WHERE productID IN ( SELECT productID FROM Product WHERE name = ?)", name)
            db.execute("DELETE FROM Product WHERE name = ?", name)
        except ValueError:
            # Incase another issue occurs
            return apology("Unfulfilled orders contain item", 400)
        return render_template("success.html")
    else:
        # Send user to form to delete products
        return render_template("remove.html")


@app.route("/orders", methods=["GET", "POST"])
@login_required
def orders():
    if request.method == "POST":
        # Get form fields
        orderId = request.form.get("orderId")
        # Check to see if the form is filled
        if not orderId:
            return apology("must provide orderId", 400)
        # Check how much stock there is if there isnt enough prevent the order from being fulfilled
        instock = db.execute(
            "SELECT Product.instock FROM Product JOIN Orders ON Product.productId = Orders.productID WHERE orderId = ?", orderId)
        if instock[0]["instock"] < 1:
            return apology("Stock must not be empty to fulfill order")
        # Update the stock and order to be fulfilled
        db.execute("UPDATE Orders SET fulfilled = 1 WHERE orderId = ?;", orderId)
        db.execute(
            "UPDATE Product SET instock = instock - 1 WHERE productID IN (SELECT productId FROM Orders WHERE orderId = ?);", orderId)
        return render_template("/portal.html")
    else:
        # Show all orders and provide option to fulfill them
        orders = db.execute(
            "SELECT Orders.orderId, Orders.orderName, Product.name, Orders.orderDate FROM Orders JOIN Product ON orders.productID = Product.productID WHERE Orders.fulfilled = 0;")
        return render_template("orders.html", orders=orders)


# Debug route for inserting a new user due to needing hashing
'''
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            if not username:
                return apology("Must provide username")
            elif not password:
                return apology("Must provide password")
            else:
                hash = generate_password_hash(password)
                db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hash)
                return redirect("/")
        except ValueError:
            return apology("Username already exists")
    else:
        return render_template("register.html")
'''
