from odonto_api.config import get_db
from odonto_api.app.models.product import Product


class ProductRepository:

    @staticmethod
    def find_product():
        collection = get_db()
        try:
            products_cursor = collection.find()  # Sin filtros
            productos_list = list(products_cursor)  # Convierte el cursor a lista

            print("Todos los productos:", productos_list)  # Mostrar productos
            print("Número de productos encontrados:", len(productos_list))
            return [Product(**product).to_dict() for product in productos_list if
                    product]  # Verifica que el producto no sea None
        except Exception as e:
            print(f"Error al buscar productos: {e}")
            return []


    #Metodo para encontrar producto por nombre
    @staticmethod
    def find_by_name(nombre):
        collection = get_db()
        try:
            query = {"nombre": {"$regex": nombre, "$options": "i"}}
            products_cursor = collection.find(query).sort("precio",1)
            productos_list = list(products_cursor)
            print("Todos los productos:", productos_list)  # Mostrar productos
            print("Número de productos encontrados:", len(productos_list))
            return [Product(**product).to_dict() for product in productos_list]
        except Exception as e:
            print(f"Error al buscar productos: {e}")
            return []



    #Metodo para encontrar producto por coincidencia marca
    @staticmethod
    def find_by_marca(marca):
        collection = get_db()
        try:
            products_cursor = collection.find({"marca": {"$regex": marca, "$options": "i"}}).sort("precio",1)
            productos_list = list(products_cursor)
            return [Product(**product).to_dict() for product in productos_list]
        except Exception as e:
            print(f"Error al buscar productos: {e}")
            return []

    #Metodo para encontrar producto por categoria
    @staticmethod
    def find_by_categoria(categoria):
        collection = get_db()
        try:
            products_cursor = collection.find({"categoria": {"$regex": categoria, "$options": "i"}}).sort("precio",1)
            productos_list = list(products_cursor)
            return [Product(**product).to_dict() for product in productos_list]
        except Exception as e:
            print(f"Error al buscar productos: {e}")
            return []




