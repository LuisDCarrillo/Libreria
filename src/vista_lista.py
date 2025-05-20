import tkinter as tk
from tkinter import ttk, messagebox
from Estudiante import Estudiante
from Lista import Lista
from collections import defaultdict
from Identificacion_estudiante import VistaIdentificacion_estudiantes
import vista_resumenAcademico as vra
from detector_duplicados import detectar_duplicados
from Pila import Pila
from DB_estudiantes import DBEstudiantes
import json

# Diccionario de materias y sus créditos
MATERIAS_CREDITOS = {
    "Calculo I": 4,
    "Calculo II": 4,
    "Calculo III": 4,
    "Calculo IV": 4,
    "Programacion I": 3,
    "Programacion II": 3,
    "Programacion III": 3,
    "Estadistica I": 4,
    "Estadistica II": 4,
    "Estadistica Matematica": 4,
    "Teoria de la Administracion I": 4,
    "Tecnicas de la Administracion II": 4,
    "Laboratorio I": 2,
    "Laboratorio II": 2,
    "Programacion Numerica": 2,
    "Programacion No Numerica I": 3,
    "Programacion No Numerica II": 4,
}
grupos_excluyentes = [
    ["Calculo I", "Calculo II", "Calculo III", "Calculo IV"],
    ["Programacion I", "Programacion II", "Programacion III"],
    ["Estadistica I", "Estadistica II", "Estadistica Matematica"],
    ["Teoria de la Administracion I", "Tecnicas de la Administracion II"],
    ["Laboratorio I", "Laboratorio II"],
    ["Programacion No Numerica I", "Programacion No Numerica II"]
]

# <-- Importar la pila

# Ruta del archivo temporal para guardar los datos
TEMP_FILE = "temp_estudiantes.json"

class VistaListaApp:
    def __init__(self, root):
        self.nodo_seleccionado = None
        self.root = root
        self.root.title("Gestión de Estudiantes")
        
        # Set window to maximized state
        self.root.state('zoomed')  # This works for both Windows and Linux/Mac

        # Create a frame to hold everything and center it
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both')

        # Scroll
        self.scroll_canvas = tk.Canvas(self.main_frame)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.scroll_canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)

        # Frame dentro del canvas donde irá todo el contenido
        self.scroll_frame = tk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw", width=self.scroll_canvas.winfo_width())

        # región scrollable
        self.scroll_frame.bind("<Configure>", self._on_frame_configure)

        # Center the content horizontally and handle resizing
        self.scroll_canvas.bind('<Configure>', self._on_canvas_configure)

        self.db = DBEstudiantes()
        
        self.lista_ingresados = self.db.Leer()
        self.lista_no_ingresados = Lista()

        self.pila_versiones = Pila()  # <-- Instancia de la pila para versiones
        
        self.titulo = tk.Label(self.main_frame, text="Gestión de Estudiantes", font=("Arial", 20))

        # 
        self.titulo = tk.Label(self.scroll_frame, text="Gestión de Estudiantes", font=("Arial", 20))
        self.titulo.pack(side="top", pady=10)

      
        self.frame_busquedas = tk.Frame(self.scroll_frame)
        self.frame_busquedas.pack(padx=10, pady=5)
        
        # Combobox que filtra por Todos e irregulares
        tk.Label(self.frame_busquedas, text="Filtrar:").grid(row=0, column=0, padx=(10, 5), sticky="w")
        self.combobox_filtro_ingresados = ttk.Combobox(
        self.frame_busquedas,
        values=["Todos", "Irregulares"],
        state="readonly",
        width=15
         )
        self.combobox_filtro_ingresados.current(0)
        self.combobox_filtro_ingresados.grid(row=0, column=1, padx=(0, 20), sticky="w")
        self.combobox_filtro_ingresados.bind("<<ComboboxSelected>>", self.filtrando_ingresados)

        #Busqueda de los ingresados
        tk.Label(self.frame_busquedas, text="Buscar Ingresados:").grid(row=0, column=2, padx=(10, 5), sticky="w")
        self.entry_buscar_ingresados = tk.Entry(self.frame_busquedas)
        self.entry_buscar_ingresados.grid(row=0, column=3, padx=(0, 50), sticky="w")
        self.entry_buscar_ingresados.bind("<KeyRelease>", self.filtrar_ingresados)
 
        # Busqueda  no ingresados
        tk.Label(self.frame_busquedas, text="Buscar No Ingresados:").grid(row=0, column=4, padx=(80, 0))
        self.entry_buscar_no_ingresados = tk.Entry(self.frame_busquedas)
        self.entry_buscar_no_ingresados.grid(row=0, column=5, padx=(20, 5))
        self.entry_buscar_no_ingresados.bind("<KeyRelease>", self.filtrar_no_ingresados)

        # Botón de "Atrás" o "Regresar" al lado del label de filtrar
        self.btn_regresar = tk.Button(self.frame_busquedas, text="Regresar", command=self.regresar)
        self.btn_regresar.grid(row=0, column=0, padx=(0, 10), sticky="w")

        # Tablas
        self.frame_tablas = tk.Frame(self.scroll_frame)
        self.frame_tablas.pack(fill="x", expand=True, padx=10)

        self.frame_tablas.grid_columnconfigure(0, weight=1)
        self.frame_tablas.grid_columnconfigure(1, weight=1)

        self.tree_ingresados = self.crear_tabla("Estudiantes Ingresados", 0)
        self.tree_no_ingresados = self.crear_tabla("Estudiantes No Ingresados", 1)

        self.contador_ingresados = tk.Label(self.frame_tablas, text="Total Ingresados: 0")
        self.contador_ingresados.grid(row=1, column=0, pady=(0, 10))

        self.contador_no_ingresados = tk.Label(self.frame_tablas, text="Total No Ingresados: 0")
        self.contador_no_ingresados.grid(row=1, column=1, pady=(0, 10))

        self.tree_ingresados.bind("<<TreeviewSelect>>", lambda e: self.autocompletar_desde_tabla(self.tree_ingresados))
        self.tree_no_ingresados.bind("<<TreeviewSelect>>", lambda e: self.autocompletar_desde_tabla(self.tree_no_ingresados))

        # Formularios
        self.frame_form = tk.Frame(self.scroll_frame)
        self.frame_form.pack(padx=10, pady=5)

        self.entries = {}
        for i, campo in enumerate(["Cédula", "Nombre", "Carrera", "Materias", "UC Aprobadas"]):
            tk.Label(self.frame_form, text=campo).grid(row=i, column=0, sticky='w')
            entry = tk.Entry(self.frame_form)
            entry.grid(row=i, column=1, pady=2, sticky='ew')
            self.entries[campo.lower()] = entry

        self.lista_destino = tk.StringVar(value="Ingresados")
        tk.Radiobutton(self.frame_form, text="Ingresados", variable=self.lista_destino, value="Ingresados").grid(row=0, column=2)
        tk.Radiobutton(self.frame_form, text="No Ingresados", variable=self.lista_destino, value="No Ingresados").grid(row=1, column=2)

        # Botones
        self.frame_btns = tk.Frame(self.scroll_frame)
        self.frame_btns.pack(pady=5)

        tk.Button(self.frame_btns, text="Agregar Estudiante", command=self.agregar_estudiante).grid(row=0, column=0, padx=5)
        tk.Button(self.frame_btns, text="Eliminar de Ingresados", command=lambda: self.eliminar_estudiante(self.lista_ingresados)).grid(row=0, column=1, padx=5)
        tk.Button(self.frame_btns, text="Eliminar de No Ingresados", command=lambda: self.eliminar_estudiante(self.lista_no_ingresados)).grid(row=0, column=2, padx=5)
        tk.Button(self.frame_btns, text="Limpiar Campos", command=self.limpiar_campos).grid(row=0, column=3, padx=5)
        tk.Button(self.frame_btns, text="Detectar Duplicados", command=lambda: detectar_duplicados(self.lista_ingresados, self.lista_no_ingresados, self.root)).grid(row=0, column=4, padx=5)

        tk.Button(self.frame_btns, text="Mover Todos a Ingresados", command=self.mover_todos_no_ingresados).grid(row=1, column=0, pady=5)
        tk.Button(self.frame_btns, text="Mover Todos a No Ingresados", command=self.mover_todos_ingresados).grid(row=1, column=1, pady=5)
        tk.Button(self.frame_btns, text="Identificacion de estudiantes", command=self.identificacion_estudiantes).grid(row=1, column=2, pady=5)
        tk.Button(self.frame_btns, text="Reportes Estadísticos", command=self.mostrar_reportes).grid(row=1, column=3, columnspan=4, pady=5)
        tk.Button(self.frame_btns, text="Ver Rendimiento Académico", command=self.ventana_rendimiento).grid(row=2, column=2, pady=5)
        ttk.Button(self.root, text="Generar Resumen Académico", command=self.abrir_vistaRA).pack(pady=50)

        btn_style = {'padx': 5, 'pady': 2, 'width': 20}

        tk.Button(self.frame_btns, text="Gestionar Materias", command=self.eliminar_materia_estudiante).grid(row=2, column=0, pady=5)

        # self.label_img_grafo = tk.Label(root)
        # self.label_img_grafo.pack(pady=10)
        # Canvas para dibujar

        self.canvas = tk.Canvas(self.main_frame, bg="white")
        # Canvas para el grafo
        self.canvas = tk.Canvas(self.scroll_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, padx=20, pady=20, expand=True)

        
        self.actualizar_tablas()

        # Botón de "Atrás" o "Regresar"
        self.btn_regresar = tk.Button(self.scroll_frame, text="Regresar", command=self.regresar)
        self.btn_regresar.pack(side="top", anchor="w", padx=10, pady=5)

        # Cargar datos guardados temporalmente
        self.cargar_datos_temporales()

    def regresar(self):
        self.root.destroy()
        
    
      

    def crear_tabla(self, titulo, col):
        frame = tk.Frame(self.frame_tablas)
        frame.grid(row=0, column=col, padx=10, sticky="nsew")
        tk.Label(frame, text=titulo).pack()
        tree = ttk.Treeview(frame, columns=("Cedula", "Nombre", "Carrera", "Materias", "UC"), show="headings", height=7)
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill="x", padx=30)
        return tree
    
    
    def identificacion_estudiantes(self):
        root = tk.Tk()
        VistaIdentificacion_estudiantes(root,self.lista_ingresados);
        root.mainloop()
        
        
    def agregar_estudiante(self):
     datos = [entry.get().strip() for entry in self.entries.values()]
     if not all(datos):
        messagebox.showwarning("Campos incompletos", "Todos los campos deben estar llenos.")
        return

     cedula, nombre, carrera, materias, uc_aprobadas = datos

     # Validaciones campos de entrada
     if not cedula.isdigit():
        messagebox.showerror("Error de Validación", "La cédula debe contener solo números.")
        return

     for lista in [self.lista_ingresados, self.lista_no_ingresados]:
        if lista.Buscar(cedula):
            messagebox.showerror("Duplicado", "La cédula ya está registrada.")
            return


     if not uc_aprobadas.isdigit():
        messagebox.showerror("Error de Validación", "Las UC Aprobadas deben ser un número.")
        return
     if not nombre.replace(" ", "").isalpha():
        messagebox.showerror("Error de Validación", "El nombre solo debe contener letras.")
        return

     materias = materias.split(",")
     materias = [materia.strip() for materia in materias]

     # Validación de materias duplicadas
     if len(materias) != len(set(materias)):
        messagebox.showerror("Error de Materia", "No se puede inscribir una misma materia más de una vez.")
        return

     creditos_totales = 0
     materias_validadas = []

     grupos_excluyentes = [
        ["Calculo I", "Calculo II", "Calculo III", "Calculo IV"],
        ["Programacion I", "Programacion II", "Programacion III"],
        ["Estadistica I", "Estadistica II", "Estadistica Matematica"],
        ["Teoria de la Administracion I", "Tecnicas de la Administracion II"],
        ["Laboratorio I", "Laboratorio II"],
        ["Programacion No Numerica I", "Programacion No Numerica II"]
     ]

     for materia in materias:
        if materia not in MATERIAS_CREDITOS:
            messagebox.showerror("Error de Materia", f"La materia {materia} no existe en el sistema.")

        cedula, nombre, carrera, materias, uc_aprobadas = datos

        estudiante = Estudiante(cedula, nombre, carrera, materias, uc_aprobadas)
        # Validaciones campos de entrada
        if not cedula.isdigit():
            messagebox.showerror("Error de Validación", "La cédula debe contener solo números.")
            return False

        if not uc_aprobadas.isdigit():
            messagebox.showerror("Error de Validación", "Las UC Aprobadas deben ser un número.")

            return
        ##########

        # Validar exclusividad por grupo
        for grupo in grupos_excluyentes:
            if materia in grupo:
                if any(m in grupo for m in materias_validadas):
                    messagebox.showerror(
                        "Error de Materia",
                        f"No se pueden inscribir juntas materias excluyentes del mismo grupo: {grupo}"
                    )
                    return

        # Verificar que los créditos no superen el límite
        creditos_totales += MATERIAS_CREDITOS[materia]
        if creditos_totales > 16:
            messagebox.showerror("Error de Créditos", "El total de créditos no puede superar 16.")
            return

        materias_validadas.append(materia)

     estudiante = Estudiante(cedula, nombre, carrera, materias, uc_aprobadas)
     estudiante.materias = materias_validadas
     estudiante.creditos_totales = creditos_totales


     destino = self.lista_ingresados if self.lista_destino.get() == "Ingresados" else self.lista_no_ingresados


     # Insertar al final de la lista usando InsDespues
     if destino.Vacia():
        destino.InsComienzo(estudiante)

     else:
        ultimo_nodo = destino.Primero
        while ultimo_nodo.prox is not None:
            ultimo_nodo = ultimo_nodo.prox
        destino.InsDespues(ultimo_nodo, estudiante)
        
     self.db.guardar(self.lista_ingresados)
     self.actualizar_tablas()
     self.limpiar_campos()

        # Guardar los datos temporalmente después de agregar un estudiante
     self.guardar_datos_temporales()


    # Filtro por Combobox para tabla ingresados 'todos' e 'irregulares' 
    def filtrando_ingresados(self, event=None):
     filtro = self.combobox_filtro_ingresados.get().lower()

     for item in self.tree_ingresados.get_children():
        self.tree_ingresados.delete(item)

    
     actual = self.lista_ingresados.Primero
     while actual:
        estudiante = actual.info 
        mostrar = True

        try:
            uc_aprobadas = int(estudiante.uc_aprobadas)
        except ValueError:
            uc_aprobadas = 0

      
        creditos_inscritos = 0
        for materia in estudiante.materias:
            if materia in MATERIAS_CREDITOS:
                creditos_inscritos += MATERIAS_CREDITOS[materia]

          #Criterio de cuando es irregular un estudiante      
        if filtro == "irregulares":
            if uc_aprobadas >= 14 and creditos_inscritos < 8:
                mostrar = True
            else:
                mostrar = False

         #Se muestran los que cumplieron con la condicion 
        if mostrar:
            self.tree_ingresados.insert('', 'end', values=(
                estudiante.cedula,
                estudiante.nombre,
                estudiante.carrera,
                ', '.join(estudiante.materias),
                estudiante.uc_aprobadas
            ))

        
        actual = actual.prox
    



    def abrir_vistaRA(self):
        nueva_ventana = tk.Toplevel(self.root)
        app_vistaRA = vra.vistaRA(nueva_ventana,self)

    def eliminar_estudiante(self, lista):
     cedula = self.entries["cédula"].get().strip()

     if lista.Vacia():
        messagebox.showinfo("Lista Vacía", "No hay estudiantes para eliminar.")
        return

     if not cedula:
        # Eliminar el último estudiante
        p = lista.Primero
        ant = None
        if p.prox is None:
            lista.EliComienzo()
        else:
            while p.prox:
                ant = p
                p = p.prox
            lista.EliDespues(ant)
        self.actualizar_tablas()
        self.limpiar_campos()
        return

    # Buscar y eliminar por cédula
     p = lista.Primero
     ant = None
     while p:
        if p.info.cedula == cedula:
            if ant:
                lista.EliDespues(ant)
            else:
                lista.EliComienzo()
            self.actualizar_tablas()
            self.limpiar_campos()
            return
        ant = p
        p = p.prox

     messagebox.showinfo("No encontrado", "Cédula no encontrada.")


    def limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.lista_destino.set("Ingresados")


    def mover_todos_no_ingresados(self):
        self.lista_ingresados.pasarListaAux(self.lista_no_ingresados, self.lista_ingresados)
        self.actualizar_tablas()

    def mover_todos_ingresados(self):
        self.lista_no_ingresados.pasarListaAux(self.lista_ingresados, self.lista_no_ingresados)
        self.actualizar_tablas()

    def autocompletar_desde_tabla(self, tree):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            for key, value in zip(self.entries.keys(), item["values"]):
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, value)

        item = tree.selection()
        if item:
            datos = tree.item(item[0])["values"]
            claves = list(self.entries.keys())
            for i in range(len(claves)):
                self.entries[claves[i]].delete(0, tk.END)
                self.entries[claves[i]].insert(0, datos[i])
            # Guardar versión anterior de materias al seleccionar
            self.cedula_seleccionada = datos[0]
            estudiante = self.lista_ingresados.Buscar(self.cedula_seleccionada)
            if estudiante:
                # Guardar copia de materias antes de modificar
                self.pila_versiones.Insertar((self.cedula_seleccionada, estudiante.info.materias))

    def deshacer_cambio_materias(self):
        # Recuperar la última versión guardada
        version = self.pila_versiones.Remover()
        if version:
            cedula, materias_anteriores = version
            nodo = self.lista_ingresados.Buscar(cedula)
            if nodo:
                # Validar restricciones antes de restaurar
                creditos_totales = sum(MATERIAS_CREDITOS[m] for m in materias_anteriores if m in MATERIAS_CREDITOS)
                if creditos_totales > 16:
                    messagebox.showerror("Error de Créditos", "No se puede deshacer porque excede el límite de créditos.")
                    return

                nodo.info.materias = materias_anteriores
                self.actualizar_tablas()
                messagebox.showinfo("Deshacer", f"Materias restauradas para el estudiante {cedula}")
            else:
                messagebox.showwarning("No encontrado", "No se encontró el estudiante para deshacer.")
        else:
            messagebox.showwarning("Sin cambios", "No hay cambios para deshacer.")

    def abrir_ventana_pilas(self, estudiante):
        import tkinter as tk
        from vista_pilas import InscripcionesApp
        ventana_pilas = tk.Toplevel(self.root)
        def actualizar_estudiante(est):
            self.actualizar_tablas()
        InscripcionesApp(ventana_pilas, estudiante, on_close=actualizar_estudiante, materias_creditos=MATERIAS_CREDITOS)

    def eliminar_materia_estudiante(self):
        cedula = self.entries["cédula"].get().strip()
        if not cedula:
            messagebox.showwarning("Cédula Vacía", "Ingrese la cédula para modificar materias.")
            return

        # Buscar estudiante en ingresados
        p = self.lista_ingresados.Primero
        while p:
            if p.info.cedula == cedula:
                self.abrir_ventana_pilas(p.info)
                return
            p = p.prox

        messagebox.showinfo("No encontrado", "Cédula no encontrada en ingresados.")

    def limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def filtrar_ingresados(self, event=None):
        texto = self.entry_buscar_ingresados.get().lower()
        self.filtrar_tabla(self.tree_ingresados, self.lista_ingresados, texto)

    def filtrar_no_ingresados(self, event=None):
        texto = self.entry_buscar_no_ingresados.get().lower()
        self.filtrar_tabla(self.tree_no_ingresados, self.lista_no_ingresados, texto)

    def filtrar_tabla(self, tree, lista, texto):
        for item in tree.get_children():
            tree.delete(item)
        p = lista.Primero
        while p:
            if texto in p.info.cedula.lower():
                tree.insert("", tk.END, values=[p.info.cedula, p.info.nombre, p.info.carrera, ", ".join(p.info.materias), p.info.uc_aprobadas])
            p = p.prox

    def actualizar_tablas(self):
        self.filtrar_ingresados()
        self.filtrar_no_ingresados()
        self.actualizar_grafo()
        self.contador_ingresados.config(text=f"Total de Ingresados: {self.lista_ingresados.Contar()}")
        self.contador_no_ingresados.config(text=f"Total de No Ingresados: {self.lista_no_ingresados.Contar()}")

    def actualizar_grafo(self):
        self.canvas.delete("all")
        if self.lista_ingresados.Vacia():
            self.canvas.create_text((self.canvas.winfo_reqwidth() / 2), (self.canvas.winfo_reqheight() / 2),
                                    text="[Lista vacía]", font=("Arial", 14))
            return

        x = 100 # Posición inicial X
        y = 150 # Posición fija Y
        separacion = 170 # Espacio entre nodos

        p = self.lista_ingresados.Primero
        while p is not None:
             # Dibujar nodo (círculo + texto)
            color = "red" if p == self.lista_ingresados.Primero else (
                "lightgreen" if p == self.nodo_seleccionado else "lightblue")
            self.canvas.create_rectangle(x - 50, y - 30, x + 50, y + 30, fill=color,
                                         tags=f"nodo_{p.info.cedula}")
            small_rect_width = 20
            self.canvas.create_rectangle(x + 50, y - 30, x + 50 + small_rect_width, y + 30, fill=color,
                                         tags=f"nodo_{p.info.cedula}")
            # Dibujar flecha si hay próximo nodo
            if p.prox is None:
                self.canvas.create_line(x + 50, y + 30, x + 50 + small_rect_width, y - 30,
                                        tags=f"nodo_{p.info.cedula}")
            self.canvas.create_text(x, y, text=str(p.info.cedula), font=("Arial", 12))

            if p.prox is not None:
                self.canvas.create_line(x + 70, y, x + separacion - 30, y, arrow=tk.LAST)
            # Etiquetar cabeza
            if p == self.lista_ingresados.Primero:
                self.canvas.create_text(x, y - 50, text="Primero", fill="red", font=("Arial", 10, "bold"))
            # Asignar evento de clic para selección
            self.canvas.tag_bind(f"nodo_{p.info.cedula}", "<Button-1>", lambda e, nodo=p: self.seleccionar_nodo(nodo))

            x += separacion
            p = p.prox
    # Selección de nodo
    def seleccionar_nodo(self, nodo):
        self.nodo_seleccionado = nodo
        self.actualizar_grafo()
    def ventana_rendimiento(self):
            ventana = tk.Toplevel(self.root)
            ventana.title("Clasificación por Rendimiento Académico")
            ventana.geometry("900x400")
    
            frame_tablas = tk.Frame(ventana)
            frame_tablas.pack(fill="both", expand=True, padx=10, pady=10)
    
            rendimiento = {
                "Alto Rendimiento": [],
                "Rendimiento Medio": [],
                "Bajo Rendimiento": []
            }
    
            def recorrer_lista(lista):
                p = lista.Primero
                while p:
                    estudiante = p.info
                    try:
                        uc = float(estudiante.uc_aprobadas)
                    except:
                        uc = 0
                    num_materias = len(estudiante.materias)
    
                    if uc >= 16 and num_materias >= 4:
                        rendimiento["Alto Rendimiento"].append(estudiante)
                    elif (12 <= uc < 16 and num_materias >= 3) or (uc >= 16 and num_materias == 3):
                        rendimiento["Rendimiento Medio"].append(estudiante)
                    else:
                        rendimiento["Bajo Rendimiento"].append(estudiante)
                    p = p.prox
    
            recorrer_lista(self.lista_ingresados)
            for i, (categoria, estudiantes) in enumerate(rendimiento.items()):
                        frame = tk.Frame(frame_tablas)
                        frame.grid(row=0, column=i, padx=5, sticky="nsew")
                        tk.Label(frame, text=categoria, font=("Arial", 12, "bold")).pack()
                        tree = ttk.Treeview(frame, columns=("Cedula", "Nombre", "Carrera", "Materias", "UC"), show="headings", height=10)
                        for col in tree["columns"]:
                            tree.heading(col, text=col)
                            tree.column(col, width=100)
                        tree.pack()
                        for est in estudiantes:
                            tree.insert("", tk.END, values=est.getInfo())
    
            for i in range(3):
                frame_tablas.grid_columnconfigure(i, weight=1)  
     

    def mostrar_reportes(self):
        reportes_window = tk.Toplevel(self.root)
        reportes_window.title("Reportes Estadísticos")
        reportes_window.geometry("900x600")

        notebook = ttk.Notebook(reportes_window)
        notebook.pack(fill=tk.BOTH, expand=True)
        

        tab_resumen = ttk.Frame(notebook)
        notebook.add(tab_resumen, text="Resumen General")
        self._crear_tab_resumen(tab_resumen)
        

        tab_carreras = ttk.Frame(notebook)
        notebook.add(tab_carreras, text="Por Carrera")
        self._crear_tab_carreras(tab_carreras)

        tab_academica = ttk.Frame(notebook)
        notebook.add(tab_academica, text="Datos Académicos")
        self._crear_tab_academica(tab_academica)
        
        

    def _crear_tab_resumen(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        total_ing = self.lista_ingresados.Contar()
        total_no_ing = self.lista_no_ingresados.Contar()
        total = total_ing + total_no_ing

        ttk.Label(frame, text="RESUMEN ESTADÍSTICO", font=('Arial', 14, 'bold')).pack(pady=10)

        metrics_frame = ttk.Frame(frame)
        metrics_frame.pack(fill=tk.X, pady=10)

        ttk.Label(metrics_frame, text=f"Total Estudiantes: {total}", font=('Arial', 12)).grid(row=0, column=0, padx=20)
        ttk.Label(metrics_frame, text=f"Ingresados: {total_ing}", font=('Arial', 12)).grid(row=0, column=1, padx=20)
        ttk.Label(metrics_frame, text=f"No Ingresados: {total_no_ing}", font=('Arial', 12)).grid(row=0, column=2,
                                                                                                 padx=20)

        if total > 0:
            # Porcentaje de INGRESADOS (verde)
            ttk.Label(
                metrics_frame,
                text=f"% Ingresados: {(total_ing / total) * 100:.1f}%",
                font=('Arial', 12),
                foreground="#4CAF50"  # Verde del gráfico
            ).grid(row=1, column=1, padx=20, pady=10)

            # Porcentaje de NO INGRESADOS (rojo)
            ttk.Label(
                metrics_frame,
                text=f"% No Ingresados: {(total_no_ing / total) * 100:.1f}%",
                font=('Arial', 12),
                foreground="#F44336"  # Rojo del gráfico
            ).grid(row=1, column=2, padx=20, pady=10)

            # Frame para contener el gráfico y asegurar que no se desborde
            graph_frame = ttk.Frame(frame)
            graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)

            # Canvas con tamaño fijo más pequeño
            canvas = tk.Canvas(graph_frame, width=300, height=250, bg='white')
            canvas.pack(pady=10)

            # Coordenadas del gráfico (ajustadas para el nuevo tamaño)
            center_x, center_y = 150, 125
            radius = 100

            start_angle = 0
            extent_ing = (total_ing / total) * 360
            extent_no_ing = (total_no_ing / total) * 360

            # Dibujar el gráfico de torta
            canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=extent_ing,
                fill="#4CAF50", outline="white"
            )
            canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle + extent_ing, extent=extent_no_ing,
                fill="#F44336", outline="white"
            )

            # Leyenda
            canvas.create_text(
                center_x, center_y + radius + 20,
                text=f"Ingresados: {total_ing} ({extent_ing / 3.6:.1f}%)",
                fill="#4CAF50", font=('Arial', 10)
            )
            canvas.create_text(
                center_x, center_y + radius + 40,
                text=f"No Ingresados: {total_no_ing} ({extent_no_ing / 3.6:.1f}%)",
                fill="#F44336", font=('Arial', 10)
            )

    def _crear_tab_carreras(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        carreras = defaultdict(int)

        for lista in [self.lista_ingresados, self.lista_no_ingresados]:
            p = lista.Primero
            while p:
                estudiante = p.info
                carrera = ""

                if hasattr(estudiante, 'carrera'):
                    carrera = estudiante.carrera
                elif hasattr(estudiante, 'getInfo'):
                    datos = estudiante.getInfo()
                    carrera = datos[2] if len(datos) > 2 else ""

                carrera = carrera.strip() if carrera else "No registrada"
                carreras[carrera] += 1
                p = p.prox

        if not carreras:
            ttk.Label(frame, text="No hay datos de carreras disponibles", font=('Arial', 12)).pack(pady=50)
            return

        tree = ttk.Treeview(frame, columns=('Carrera', 'Total', '%'), show='headings')
        tree.heading('Carrera', text='Carrera')
        tree.heading('Total', text='Total')
        tree.heading('%', text='%')

        tree.column('Carrera', width=400)
        tree.column('Total', width=150, anchor='center')
        tree.column('%', width=150, anchor='center')

        total_estudiantes = sum(carreras.values())

        for carrera, total in sorted(carreras.items(), key=lambda x: x[1], reverse=True):
            porcentaje = (total / total_estudiantes) * 100 if total_estudiantes > 0 else 0

            tree.insert('', 'end', values=(
                carrera,
                total,
                f"{porcentaje:.1f}%"
            ))

        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        if carreras:
            canvas = tk.Canvas(frame, width=800, height=300, bg='white')
            canvas.pack(pady=20)

            max_cant = max(carreras.values())
            x = 50
            bar_width = 40
            spacing = 20

            for i, (carrera, total) in enumerate(sorted(carreras.items(), key=lambda x: x[1], reverse=True)[:10]):
                height = (total / max_cant) * 250
                color = "#{:06x}".format(i * 0x333333 % 0xFFFFFF)

                canvas.create_rectangle(x, 280 - height, x + bar_width, 280, fill=color, outline='black')
                canvas.create_text(x + bar_width / 2, 290, text=carrera[:15] + ("..." if len(carrera) > 15 else ""),
                                   angle=45, anchor='ne')
                canvas.create_text(x + bar_width / 2, 280 - height - 10, text=str(total))
                x += bar_width + spacing

    def _crear_tab_academica(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(frame, text="DATOS ACADÉMICOS", font=('Arial', 14, 'bold')).pack(pady=10)

        # --- 1. Tabla de frecuencia de materias (nueva) ---
        frame_frecuencia = ttk.LabelFrame(frame, text="Materias Inscritas (Frecuencia)")
        frame_frecuencia.pack(fill=tk.X, padx=10, pady=5)

        tree_frecuencia = ttk.Treeview(frame_frecuencia, columns=("Materia", "Créditos", "Estudiantes"),
                                       show="headings")
        tree_frecuencia.heading("Materia", text="Materia")
        tree_frecuencia.heading("Créditos", text="Créditos")
        tree_frecuencia.heading("Estudiantes", text="Estudiantes")
        tree_frecuencia.column("Materia", width=200)
        tree_frecuencia.column("Créditos", width=80, anchor="center")
        tree_frecuencia.column("Estudiantes", width=100, anchor="center")
        tree_frecuencia.pack(fill=tk.X, padx=10, pady=5)

        # Contar estudiantes por materia
        frecuencia_materias = {}
        actual = self.lista_ingresados.Primero
        while actual:
            for materia in actual.info.materias:
                frecuencia_materias[materia] = frecuencia_materias.get(materia, 0) + 1
            actual = actual.prox

        # Llenar tabla (ordenada por frecuencia)
        for materia, estudiantes in sorted(frecuencia_materias.items(), key=lambda x: x[1], reverse=True):
            creditos = MATERIAS_CREDITOS.get(materia, "N/A")
            tree_frecuencia.insert("", "end", values=(materia, creditos, estudiantes))

        # --- 2. Créditos por estudiante (sección existente) ---
        frame_creditos = ttk.LabelFrame(frame, text="Créditos Totales por Estudiante")
        frame_creditos.pack(fill=tk.X, padx=10, pady=5)

        tree_creditos = ttk.Treeview(frame_creditos, columns=("Estudiante", "Créditos"), show="headings")
        tree_creditos.heading("Estudiante", text="Estudiante (Cédula)")
        tree_creditos.heading("Créditos", text="Créditos")
        tree_creditos.column("Estudiante", width=250)
        tree_creditos.column("Créditos", width=100, anchor="center")
        tree_creditos.pack(fill=tk.X, padx=10, pady=5)

        # Llenar tabla de créditos por estudiante
        actual = self.lista_ingresados.Primero
        while actual:
            estudiante = actual.info
            creditos_totales = sum(MATERIAS_CREDITOS.get(materia, 0) for materia in estudiante.materias)
            tree_creditos.insert("", "end", values=(
                f"{estudiante.nombre} ({estudiante.cedula})",
                creditos_totales
            ))
            actual = actual.prox

        # --- 3. Resumen de créditos (existente) ---
        frame_resumen = ttk.LabelFrame(frame, text="Resumen de Créditos")
        frame_resumen.pack(fill=tk.X, padx=10, pady=5)

        total_creditos = sum(
            MATERIAS_CREDITOS.get(materia, 0)
            for estudiante in self.lista_ingresados.obtener_todos()
            for materia in estudiante.materias
        )
        promedio_creditos = total_creditos / self.lista_ingresados.Contar() if self.lista_ingresados.Contar() > 0 else 0

        ttk.Label(frame_resumen, text=f"Total de créditos inscritos: {total_creditos}", font=('Arial', 10)).pack(
            anchor="w", padx=5, pady=2)
        ttk.Label(frame_resumen, text=f"Promedio de créditos por estudiante: {promedio_creditos:.1f}",
                  font=('Arial', 10)).pack(anchor="w", padx=5, pady=2)
    def cargar_datos_temporales(self):
        """Carga los datos de los estudiantes desde un archivo JSON temporal."""
        try:
            with open(TEMP_FILE, "r") as file:
                datos = json.load(file)
                for estudiante_data in datos.get("ingresados", []):
                    estudiante = Estudiante(
                        estudiante_data["cedula"],
                        estudiante_data["nombre"],
                        estudiante_data["carrera"],
                        estudiante_data["materias"],
                        estudiante_data["uc_aprobadas"]
                    )
                    self.lista_ingresados.InsComienzo(estudiante)

                for estudiante_data in datos.get("no_ingresados", []):
                    estudiante = Estudiante(
                        estudiante_data["cedula"],
                        estudiante_data["nombre"],
                        estudiante_data["carrera"],
                        estudiante_data["materias"],
                        estudiante_data["uc_aprobadas"]
                    )
                    self.lista_no_ingresados.InsComienzo(estudiante)

                self.actualizar_tablas()
        except FileNotFoundError:
            pass

    def _on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Update the frame width when the canvas is resized"""
        # Update the width of the frame to match the canvas width
        self.scroll_canvas.itemconfig(self.scroll_canvas.find_withtag("all")[0], width=event.width)

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaListaApp(root)
    root.mainloop()
