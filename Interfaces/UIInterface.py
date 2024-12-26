
from Interfaces.CommandInterface import UserInterface
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SpreadsheetController import SpreadsheetController

import tkinter as tk
from tkinter import ttk
import string

class UI(UserInterface):
    def __init__(self, controller: 'SpreadsheetController'):
        self.controller = controller
        self.controller.new_spreadsheet()
        
        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("Spreadsheet Editor")
        self.root.geometry("800x600")
        
        # Crear el menú
        self.create_menu()
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para la entrada de fórmulas
        formula_frame = ttk.Frame(main_frame)
        formula_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Etiqueta para mostrar la celda seleccionada
        self.selected_cell_label = ttk.Label(formula_frame, text="A1")
        self.selected_cell_label.pack(side=tk.LEFT, padx=5)
        
        # Entrada para fórmulas
        self.formula_entry = ttk.Entry(formula_frame)
        self.formula_entry.pack(fill=tk.X, expand=True, padx=5)
        
        # Frame para la cuadrícula
        grid_frame = ttk.Frame(main_frame)
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear scrollbars
        x_scrollbar = ttk.Scrollbar(grid_frame, orient=tk.HORIZONTAL)
        y_scrollbar = ttk.Scrollbar(grid_frame)
        
        # Crear el widget Treeview para la cuadrícula
        self.grid = ttk.Treeview(grid_frame, show="headings", 
                                yscrollcommand=y_scrollbar.set,
                                xscrollcommand=x_scrollbar.set)
        
        # Configurar scrollbars
        x_scrollbar.config(command=self.grid.xview)
        y_scrollbar.config(command=self.grid.yview)
        
        # Posicionar elementos
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.grid.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurar columnas y filas
        self.setup_grid()
        
        # Vincular eventos
        self.grid.bind('<ButtonRelease-1>', self.cell_clicked)
        self.formula_entry.bind('<Return>', self.formula_entered)
        
        # Estilo
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, selectmode="browse")
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        style.map("Treeview",
            background=[("selected", "#0078D7")],
            foreground=[("selected", "white")])
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
    def setup_grid(self):
        # Configurar columnas (A-Z)
        columns = list(string.ascii_uppercase)[:26]  # A-Z
        self.grid["columns"] = columns
        
        for col in columns:
            self.grid.heading(col, text=col)
            self.grid.column(col, width=100, minwidth=50)
        
        # Insertar filas (1-100)
        for i in range(1, 101):
            self.grid.insert("", tk.END, values=[""] * len(columns), tags=(str(i),))
    
    def cell_clicked(self, event):
        item = self.grid.selection()[0]
        column = self.grid.identify_column(event.x)
        row = self.grid.item(item)["tags"][0]
        
        # Convertir número de columna a letra (1 -> A, 2 -> B, etc.)
        col_letter = string.ascii_uppercase[int(column[1]) - 1]
        cell_coord = f"{col_letter}{row}"
        
        self.selected_cell_label.config(text=cell_coord)
        
        # Mostrar contenido en la entrada de fórmulas
        content = self.controller.get_cell_formula_expression(cell_coord)
        self.formula_entry.delete(0, tk.END)
        self.formula_entry.insert(0, content if content else "")
    
    def formula_entered(self, event):
        cell_coord = self.selected_cell_label.cget("text")
        content = self.formula_entry.get()
        
        # Actualizar el contenido de la celda
        self.controller.set_cell_content(cell_coord, content)
        
        # Actualizar la visualización
        row_num = int(cell_coord[1:])
        col_letter = cell_coord[0]
        col_index = string.ascii_uppercase.index(col_letter)
        
        item = self.grid.get_children()[row_num - 1]
        current_values = list(self.grid.item(item)["values"])
        current_values[col_index] = self.controller.get_cell_content_as_float(cell_coord)
        self.grid.item(item, values=current_values)
    
    def new_file(self):
        self.controller.new_spreadsheet()
        self.clear_grid()
    
    def open_file(self):
        # Aquí podrías agregar un diálogo de selección de archivo
        self.controller.load_spreadsheet_from_file("example.sheet")
        self.update_grid()
    
    def save_file(self):
        # Aquí podrías agregar un diálogo de guardado
        self.controller.save_spreadsheet_to_file("example.sheet")
    
    def clear_grid(self):
        for item in self.grid.get_children():
            self.grid.item(item, values=[""] * 26)
    
    def update_grid(self):
        # Actualizar el grid con los datos del spreadsheet
        # Esta función necesitaría ser implementada según la estructura de datos de tu Spreadsheet
        pass
    
    def run(self):
        self.root.mainloop()

# Ejemplo de uso:
if __name__ == "__main__":
    controller = SpreadsheetController()
    app = UI(controller)
    app.run()