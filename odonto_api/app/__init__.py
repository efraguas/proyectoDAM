from flask import Flask
from odonto_api.app.controllers.product_controller import product


def create_app():
    app = Flask(__name__)
    #registrar rutas
    app.register_blueprint(product)
    return app