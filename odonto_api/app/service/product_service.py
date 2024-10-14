from bson import ObjectId

from odonto_api.app.models.product import Product
from odonto_api.app.repository.product_repository import ProductRepository


class ProductService:

    @staticmethod
    def get_all():
        try:
            products = ProductRepository.find_product()
            print("Todos los productos:", products)  # Mostrar productos
            print("Número de productos encontrados:", len(products))
            return [Product(**product).to_dict() for product in products if
                    product]  # Verifica que el producto no sea None
        except Exception as e:
            print(f"Error al buscar productos: {e}")
            return []

    @staticmethod
    def get_by_id(id):
        try:
            product = ProductRepository.find_by_id(id)
            return Product(**product).to_dict()
        except Exception as e:
            print(f"Error al buscar productos: {e}")
            return []

    @staticmethod
    def get_by_name(nombre):
        try:
            products = ProductRepository.find_by_name(nombre)
            print("Todos los productos:", products)  # Mostrar productos
            print("Número de productos encontrados:", len(products))
            return [Product(**product).to_dict() for product in products]
        except Exception as e:
            print(f"Error al buscar productos: {e}")
            return []

    @staticmethod
    def get_by_marca(marca):
        try:
            products = ProductRepository.find_by_marca(marca)
            print("Todos los productos:", products)  # Mostrar productos
            print("Número de productos encontrados:", len(products))
            return [Product(**product).to_dict() for product in products]
        except Exception as e:
            print(f"Error al buscar productos: {e}")
            return []

    @staticmethod
    def get_by_categoria(categoria):
        try:
            products = ProductRepository.find_by_categoria(categoria)
            print("Todos los productos:", products)  # Mostrar productos
            print("Número de productos encontrados:", len(products))
            return [Product(**product).to_dict() for product in products if
                product] # Verifica que el producto no sea None
        except Exception as e:
            print(f"Error al buscar productos: {e}")
            return []




