from bson import ObjectId

from odonto_api.config import get_db

class ProductRepository:





    @staticmethod
    def find_product():
        collection = get_db()
        try:
            products_cursor = collection.find()  # Sin filtros
            productos_list = list(products_cursor)  # Convierte el cursor a lista
            return productos_list
        except Exception as e:
            raise e

    # Metodo para encontrar producto por nombre
    @staticmethod
    def find_by_id(id):
        collection = get_db()
        try:
            product= collection.find_one({'_id': ObjectId(id)})
            return product
        except Exception as e:
            raise e

    #Metodo para encontrar producto por nombre
    @staticmethod
    def find_by_name(nombre):
        collection = get_db()
        try:
            query = {"nombre": {"$regex": nombre, "$options": "i"}}
            products_cursor = collection.find(query).sort("precio",1)
            productos_list = list(products_cursor)
            return productos_list
        except Exception as e:
            raise e



    #Metodo para encontrar producto por coincidencia marca
    @staticmethod
    def find_by_marca(marca):
        collection = get_db()
        try:
            query = {"marca": {"$regex": marca, "$options": "i"}}
            products_cursor = collection.find(query).sort("precio",1)
            productos_list = list(products_cursor)
            return productos_list
        except Exception as e:
            raise e

    #Metodo para encontrar producto por categoria
    @staticmethod
    def find_by_categoria(categoria):
        collection = get_db()
        try:
            query = {"categoria": {"$regex": categoria, "$options": "i"}}
            products_cursor = collection.find(query).sort("precio",1)
            productos_list = list(products_cursor)
            return productos_list
        except Exception as e:
            raise e




