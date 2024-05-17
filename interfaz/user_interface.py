import tkinter as tk
import tkinter.messagebox as messagebox
from pymongo import MongoClient

#Interfaz de usuario de a la aplicacion
class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Productos Odontológicos")

        # Conexión a la base de datos MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["Materiales_odontologia"]
        self.collections = ['antonSD', 'Proclinic', 'dental_Iberica']

        # Etiqueta y entrada para el nombre del producto
        tk.Label(self.root, text="Nombre del Producto:").grid(row=0, column=0, padx=10, pady=5)
        self.entrada_producto = tk.Entry(self.root)
        self.entrada_producto.grid(row=0, column=1, padx=10, pady=5)

        # Botón de búsqueda
        self.boton_buscar = tk.Button(self.root, text="Buscar", command=self.buscar_productos)
        self.boton_buscar.grid(row=0, column=6, padx=10, pady=5)

        # Cuadro de texto para mostrar los resultados
        self.resultados = tk.Text(self.root, height=10, width=100)
        self.resultados.grid(row=1, columnspan=6, padx=10, pady=5)

    def buscar_productos(self):
        self.resultados.delete("1.0", tk.END)  # Limpiar resultados anteriores
        producto = self.entrada_producto.get()

        #filtor para quitar campos nulos

        filtrar = {
            "$and": [
                {"nombre": {"$regex": producto, "$options": "i"}},
                {"nombre": {"$ne": None}},
                {"marca": {"$ne": None}},
                {"categoria": {"$ne": None}},
                {"subcategoria": {"$ne": None}},
                {"precio": {"$ne": None}},
                {"url": {"$ne": None}}
            ]
        }

        # Realizar la búsqueda en la base de datos y mostrar los resultados
        if producto:
            for coleccion in self.collections:
                collection = self.db[coleccion]
                resultados = collection.find(filtrar).sort("precio", 1)

                for item in resultados:
                    nombre = item["nombre"]
                    categoria = item.get("categoria", "N/A")
                    subcategoria = item.get("subcategoria", "N/A")
                    precio = item.get("precio", "N/A")
                    url = item.get("url", "N/A")

                    self.resultados.insert(tk.END, f"Nombre: {nombre}\n")
                    self.resultados.insert(tk.END, f"Categoría: {categoria}\n")
                    self.resultados.insert(tk.END, f"Subcategoría: {subcategoria}\n")
                    self.resultados.insert(tk.END, f"Precio: {precio}\n\n")
                    self.resultados.insert(tk.END, f"WEb: {url}\n\n")
        else:
            tk.messagebox.showerror("Error", "Por favor, introduzca el nombre del producto.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
