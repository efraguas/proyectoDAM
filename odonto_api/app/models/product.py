from bson import ObjectId


class Product:
    def __init__(self,**data):
        self._id = str(data.get('_id')) if isinstance(data.get('_id'),ObjectId) else data.get('_id')
        self.nombre = data.get('nombre')
        self.marca = data.get('marca')
        self.categoria = data.get('categoria')
        self.precio = data.get('precio')
        self.url = data.get('url')
        self.subcategoria = data.get('subcategoria', 'none')

    #Metodo para convertir el valor precio a float si es un string
    @staticmethod
    def convert_precio(precio):
        try:
            return float(precio)
        except (ValueError, TypeError):
            return 0.0


    #Metodo para convertir Product en un diccionario:
    def to_dict(self):
        return {
            '_id': self._id,
            'nombre': self.nombre,
            'marca': self.marca,
            'categoria': self.categoria,
            'subcategoria': self.subcategoria,
            'precio': self.precio,
            'url': self.url
        }