from flask import Blueprint, request, jsonify
from odonto_api.app.service.product_service import ProductService

product = Blueprint('product', __name__)

#Endopoint para obtener todos los productos
@product.route( '/productos', methods=['GET'])
def get_products():
    producto = ProductService.get_all()
    return jsonify(producto), 200

# Endpoint para obtener producto filtrado por coincicencia en nombre y ordenado por precio ASC
@product.route('/productos/nombre', methods=['GET'])
def get_name():
    nombre = request.args.get('nombre')  # Captura del nombre parcial desde query params
    producto = ProductService.get_by_name(nombre)
    return jsonify(producto), 200


#Endopoint para obtener producto filtrado por categoria y ordenado por precio ASC
@product.route('/productos/categoria', methods=['GET'])
def get_category():
    categoria = request.args.get('categoria')
    producto = ProductService.get_by_categoria(categoria)
    return jsonify(producto), 200

#Endopoint para obtener filtrado por marca y ordenado por precio ASC
@product.route('/productos/marca', methods=['GET'])
def get_marca():
    marca = request.args.get('marca')
    producto = ProductService.get_by_marca(marca)
    return jsonify(producto), 200