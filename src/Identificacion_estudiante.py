import tkinter as tk
from tkinter import ttk, messagebox
from Estudiante import Estudiante
from Lista import Lista 

class VistaIdentificacion_estudiantes:
    def __init__(self, root, lista):
        self.nodo_seleccionado = None
        
        self.root = root
        self.root.title("Gestión de Estudiantes")
        self.root.minsize(1000, 800)

        self.lista = lista
        
        self.lista_excesivo = Lista()
        self.lista_medio = Lista()
        self.lista_bajo = Lista()
        
        self.titulo = tk.Label(self.root, text="Clasificación de estudiantes", font=("Arial", 20))
        self.titulo.pack(side="top", pady=10)

        self.frame_tablas = tk.Frame(root)
        self.frame_tablas.pack(fill="x", expand=True, padx=10)
        
        self.frame_tablas.grid_columnconfigure(0, weight=1)

        self.tree_excesivos = self.crear_tabla("Estudiantes con cargas academicas altas", 0)
        self.tree_medios = self.crear_tabla("Estudiantes con cargas academicas normales", 1)
        self.tree_bajos = self.crear_tabla("Estudiantes con cargas academicas bajas", 2)

        self.actualizar_tablas()

    def crear_tabla(self, titulo, col):
        frame = tk.Frame(self.frame_tablas)
        frame.grid(row=col, column=0, padx=10, sticky="nsew")
        tk.Label(frame, text=titulo).pack()
        tree = ttk.Treeview(frame, columns=("Cedula", "Nombre", "Carrera", "cantidad de materias", "UC acumuladas", "UC actuales"), show="headings", height=8)
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill="x", padx=30, pady=(10,60))
        return tree
    
    
    def filtrar_ingresados(self, event=None):
        # texto = self.entry_buscar_ingresados.get().lower()
        self.filtrar_tabla()

    def filtrar_tabla(self):
        for item in self.tree_excesivos.get_children():
            self.tree_excesivos.delete(item)
        for item in self.tree_medios.get_children():
            self.tree_medios.delete(item)
        for item in self.tree_bajos.get_children():
            self.tree_bajos.delete(item)
            
        p = self.lista.Primero
        
        while p:
            informacion  = p.info.getInfo()
            
            informacion[3] = len(p.info.materias)
            informacion.append(p.info.creditos_totales)
            if p.info.creditos_totales >= 14 and len(p.info.materias) >= 4:
                self.tree_excesivos.insert("", tk.END, values=informacion)
            elif p.info.creditos_totales < 8 and len(p.info.materias) <= 3:
                self.tree_bajos.insert("", tk.END, values=informacion)
            else: 
                self.tree_medios.insert("", tk.END, values=informacion)
            p = p.prox
            

    def actualizar_tablas(self):
        self.filtrar_ingresados()

