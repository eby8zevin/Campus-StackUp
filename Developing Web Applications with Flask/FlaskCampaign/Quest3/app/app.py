from flask import Flask, request, render_template, redirect, url_for
from models import Product, User, db
from controllers.users import get_users, get_user, add_user, update_user, delete_user, get_user_by_username
from controllers.products import get_products, get_product, add_product, update_product, delete_product
from sqlalchemy import exc
import hashlib
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import secrets

app = Flask(__name__, template_folder = 'templates', static_folder = 'static')
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

shopname = "AhmadAbuHasan-Shop"

products = [
    {
        'id': 1,
        'title': 'Big Apple',
        'description': 'A big apple',
        'price': 5,
        'category': 'Fruit',
        'image': 'bigapple.jpg'
    },
    {
        'id': 2,
        'title': 'Cool Flask',
        'description': 'A flask that is cool',
        'price': 10,
        'category': 'Water Bottles',
        'image': 'coolflask.jpg'
    },
    {
        'id': 3,
        'title': 'Cat Mouse',
        'description': 'A cat shaped mouse',
        'price': 15,
        'category': 'Electronics',
        'image': 'catmouse.jpg'
    }
]

users = [
    {
        'id': 1,
        'username': 'admin',
        'password': '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',
        'email': 'admin@stackshop.com',
        'role': 'admin'
    }
]

with app.app_context():
    db.create_all()
    try:
        for product in products:
            new_product = Product(
                id = product['id'],
                title = product['title'],
                description = product['description'],
                price = product['price'],
                category = product['category'],
                image = product['image']
            )
            db.session.add(new_product)
        db.session.commit()

    except exc.IntegrityError:
        db.session.rollback()
        print('Products already exist in database')

    try:
        for user in users:
            new_user = User(
                id = user['id'],
                username = user['username'],
                password = user['password'],
                email = user['email'],
                role = user['role']
            )
            db.session.add(new_user)
        db.session.commit()

    except exc.IntegrityError:
        db.session.rollback()
        print('Users already exist in database')