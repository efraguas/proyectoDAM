import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import requests


class ComparOdontoUI:
    def __init__(self, interfaz):
        self.interfaz = interfaz
        self.interfaz.title("Comparador de Productos Odontológicos")
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")

        # Url de la api
        self.api_url = "http://localhost:8080/api/odonto_api"

        # Configuración de la desktop_app
        self.frame = tk.Frame(interfaz)
        self.frame.pack(expand=True, pady=10, fill=tk.BOTH)

        # Etiqueta "Articulo a buscar"
        self.label = tk.Label(self.frame, text="Busqueda:")
        self.label.pack(side=tk.LEFT, padx=(0, 5))

        # Campo de texto
        self.entry = tk.Entry(self.frame, width=50)
        self.entry.pack(expand=True, side=tk.LEFT, padx=10, fill=tk.X)

        # Botón de búsqueda
        self.button = tk.Button(self.frame, text="Buscar", command=self.buscar, width=30)
        self.button.pack(side=tk.LEFT)
        self.entry.bind("<Return>", lambda event: self.buscar())

        # Tabla para mostrar resultados
        self.columns = ("Nombre", "Categoria", "Subcategoria", "Precio", "url")
        self.tree = ttk.Treeview(interfaz, columns=self.columns, show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Categoria", text="Categoría")
        self.tree.heading("Subcategoria", text="Subcategoría")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("url", text="URL")

        # Configurar Scrollbar vertical
        self.scrollbar = ttk.Scrollbar(interfaz, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.pack(expand=True, pady=10, fill=tk.BOTH)

        # Asociar el evento de clic en la columna URL con la función abrir_url
        self.tree.bind('<ButtonRelease-1>', self.abrir_url)

    # Funcion de busqueda/ordenacion de los productos por precio
    def buscar(self):
        texto = self.entry.get()
        if not texto:
            messagebox.showerror("Error", "El campo de texto no puede estar vacío.")
            return

        # Funcion para llamar a la API
        try:
            response = requests.get(f"{self.api_url}/nombre", params={"nombre": texto})
            response.raise_for_status()
            resultados = response.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f'Error de conexion a API: {e}')
            return

        # Limpiar la tabla
        for fila in self.tree.get_children():
            self.tree.delete(fila)

        # Mostrar resultados en la tabla
        for doc in resultados:
            self.tree.insert("", "end", values=(doc["nombre"], doc["categoria"], doc["subcategoria"],
                                                doc["precio"], doc["url"]))

    # Funcion para visitar la url del producto seleccionado
    def abrir_url(self, event):
        item = self.tree.identify('item', event.x, event.y)
        column = self.tree.identify_column(event.x)
        if column == '#5':  # columna de la URL
            url = self.tree.item(item, "values")[4]
            webbrowser.open(url)

def main():
    interfaz = tk.Tk()
    app = ComparOdontoUI(interfaz)
    interfaz.mainloop()

if __name__ == "__main__":
    main()
