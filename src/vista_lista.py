import tkinter as tk
from tkinter import ttk, messagebox
from Estudiante import Estudiante
from Lista import Lista
from collections import defaultdict
from Identificacion_estudiante import VistaIdentificacion_estudiantes
import vista_resumenAcademico as vra

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

class VistaListaApp:
    def __init__(self, root):
        self.nodo_seleccionado = None

        self.root = root
        self.root.title("Gestión de Estudiantes")

        self.lista_ingresados = Lista()
        self.lista_no_ingresados = Lista()

        self.titulo = tk.Label(self.root, text="Gestión de Estudiantes", font=("Arial", 20))
        self.titulo.pack(side="top", pady=10)

        self.frame_busquedas = tk.Frame(root)
        self.frame_busquedas.pack(padx=10, pady=5)
        # Busqueda de los ingresados
        tk.Label(self.frame_busquedas, text="Buscar Ingresados:").grid(row=0, column=0)
        self.entry_buscar_ingresados = tk.Entry(self.frame_busquedas)
        self.entry_buscar_ingresados.grid(row=0, column=1, padx=(5, 50))
        self.entry_buscar_ingresados.bind("<KeyRelease>", self.filtrar_ingresados)
        # Busqueda no ingresados
        tk.Label(self.frame_busquedas, text="Buscar No Ingresados:").grid(row=0, column=4, padx=(80, 0))
        self.entry_buscar_no_ingresados = tk.Entry(self.frame_busquedas)
        self.entry_buscar_no_ingresados.grid(row=0, column=5, padx=(20, 5))
        self.entry_buscar_no_ingresados.bind("<KeyRelease>", self.filtrar_no_ingresados)

        self.frame_tablas = tk.Frame(root)
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
        self.tree_no_ingresados.bind("<<TreeviewSelect>>",
                                     lambda e: self.autocompletar_desde_tabla(self.tree_no_ingresados))

        self.frame_form = tk.Frame(root)
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
        
        tk.Radiobutton(self.frame_form, text="Ingresados", variable=self.lista_destino, value="Ingresados").grid(row=0,
                                                                                                                 column=2)
        tk.Radiobutton(self.frame_form, text="No Ingresados", variable=self.lista_destino, value="No Ingresados").grid(
            row=1, column=2)

        self.frame_btns = tk.Frame(root)
        self.frame_btns.pack(pady=5)



        tk.Button(self.frame_btns, text="Agregar Estudiante", command=self.agregar_estudiante).grid(row=0, column=0, padx=5)
        tk.Button(self.frame_btns, text="Eliminar de Ingresados", command=lambda: self.eliminar_estudiante(self.lista_ingresados)).grid(row=0, column=1, padx=5)
        tk.Button(self.frame_btns, text="Eliminar de No Ingresados", command=lambda: self.eliminar_estudiante(self.lista_no_ingresados)).grid(row=0, column=2, padx=5)
        tk.Button(self.frame_btns, text="Limpiar Campos", command=self.limpiar_campos).grid(row=0, column=3, padx=5)

        tk.Button(self.frame_btns, text="Mover Todos a Ingresados", command=self.mover_todos_no_ingresados).grid(row=1, column=0, pady=5)
        tk.Button(self.frame_btns, text="Mover Todos a No Ingresados", command=self.mover_todos_ingresados).grid(row=1, column=1, pady=5)
        tk.Button(self.frame_btns, text="Identificacion de estudiantes", command=self.identificacion_estudiantes).grid(row=1, column=2, pady=5)
        tk.Button(
            self.frame_btns,
            text="Reportes Estadísticos",
            command=self.mostrar_reportes
        ).grid(row=1, column=3, columnspan=4, pady=5)

        #Botón para abrir la vista de resumen academico
        ttk.Button(self.root, text="Generar Resumen Académico", command=self.abrir_vistaRA).pack(pady=50)

        btn_style = {'padx': 5, 'pady': 2, 'width': 20}

       
        

        # self.label_img_grafo = tk.Label(root)
        # self.label_img_grafo.pack(pady=10)
        # Canvas para dibujar

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, padx=20, pady=20, expand=True)

        self.actualizar_tablas()

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

     # Validar que la cédula no esté repetida en ninguna lista
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
            return
        if not uc_aprobadas.isdigit():
            messagebox.showerror("Error de Validación", "Las UC Aprobadas deben ser un número.")

            return

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

     self.actualizar_tablas()
     self.limpiar_campos()

    #Función para abrir la vista de resumen académico
    def abrir_vistaRA(self):
        nueva_ventana = tk.Toplevel(self.root)
        app_vistaRA = vra.vistaRA(nueva_ventana, self)

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
        if p.info.identificacion == cedula:
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

    def actualizar_tablas(self):
        for tree, lista in [(self.tree_ingresados, self.lista_ingresados), (self.tree_no_ingresados, self.lista_no_ingresados)]:
            for item in tree.get_children():
                tree.delete(item)

            for estudiante in lista.obtener_todos():
                tree.insert("", "end", values=(estudiante.cedula, estudiante.nombre, estudiante.carrera, ", ".join(estudiante.materias), estudiante.uc_aprobadas))

        self.contador_ingresados.config(text=f"Total Ingresados: {self.lista_ingresados.obtener_tamano()}")
        self.contador_no_ingresados.config(text=f"Total No Ingresados: {self.lista_no_ingresados.obtener_tamano()}")

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
            if texto in p.info.identificacion.lower():
                tree.insert("", tk.END, values=[p.info.identificacion, p.info.nombre, p.info.edad,", ".join(p.info.materias), p.info.uc_aprobadas])
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
                                         tags=f"nodo_{p.info.identificacion}")
            small_rect_width = 20
            self.canvas.create_rectangle(x + 50, y - 30, x + 50 + small_rect_width, y + 30, fill=color,
                                         tags=f"nodo_{p.info.identificacion}")
            # Dibujar flecha si hay próximo nodo
            if p.prox is None:
                self.canvas.create_line(x + 50, y + 30, x + 50 + small_rect_width, y - 30,
                                        tags=f"nodo_{p.info.identificacion}")
            self.canvas.create_text(x, y, text=str(p.info.identificacion), font=("Arial", 12))

            if p.prox is not None:
                self.canvas.create_line(x + 70, y, x + separacion - 30, y, arrow=tk.LAST)
            # Etiquetar cabeza
            if p == self.lista_ingresados.Primero:
                self.canvas.create_text(x, y - 50, text="Primero", fill="red", font=("Arial", 10, "bold"))
            # Asignar evento de clic para selección
            self.canvas.tag_bind(f"nodo_{p.info}", "<Button-1>", lambda e, nodo=p: self.seleccionar_nodo(nodo))

            x += separacion
            p = p.prox
    # Selección de nodo
    def seleccionar_nodo(self, nodo):
        self.nodo_seleccionado = nodo
        self.actualizar_grafo()

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
            ttk.Label(metrics_frame, text=f"% Ingresados: {(total_ing / total) * 100:.1f}%", font=('Arial', 12)).grid(
                row=1, column=1, pady=10)

        if total > 0:
            canvas = tk.Canvas(frame, width=400, height=300, bg='white')
            canvas.pack(pady=20)

            start_angle = 0
            extent_ing = (total_ing / total) * 360
            extent_no_ing = (total_no_ing / total) * 360

            canvas.create_arc(50, 50, 350, 350, start=start_angle, extent=extent_ing, fill="#4CAF50", outline="white")
            canvas.create_arc(50, 50, 350, 350, start=start_angle + extent_ing, extent=extent_no_ing, fill="#F44336",
                              outline="white")

            canvas.create_text(200, 400, text=f"Ingresados: {total_ing} ({extent_ing / 3.6:.1f}%)", fill="#4CAF50",
                               font=('Arial', 10))
            canvas.create_text(200, 420, text=f"No Ingresados: {total_no_ing} ({extent_no_ing / 3.6:.1f}%)",
                               fill="#F44336", font=('Arial', 10))

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

        uc_aprobadas = []
        materias = defaultdict(int)

        for lista in [self.lista_ingresados, self.lista_no_ingresados]:
            p = lista.Primero
            while p:
                if hasattr(p.info, 'uc_aprobadas'):
                    try:
                        uc_aprobadas.append(int(p.info.uc_aprobadas))
                    except:
                        pass
                if hasattr(p.info, 'materias'):

                    materias[", ".join(p.info.materias)] += 1

                    materias[p.info.materias] += 1

                p = p.prox

        ttk.Label(frame, text="DATOS ACADÉMICOS", font=('Arial', 14, 'bold')).pack(pady=10)

        if uc_aprobadas:
            stats_frame = ttk.Frame(frame)
            stats_frame.pack(fill=tk.X, pady=10)

            ttk.Label(stats_frame, text=f"UC aprobadas (promedio): {sum(uc_aprobadas) / len(uc_aprobadas):.1f}",
                      font=('Arial', 10)).pack(side=tk.LEFT, padx=20)
            ttk.Label(stats_frame, text=f"Mínimo: {min(uc_aprobadas)}", font=('Arial', 10)).pack(side=tk.LEFT, padx=20)
            ttk.Label(stats_frame, text=f"Máximo: {max(uc_aprobadas)}", font=('Arial', 10)).pack(side=tk.LEFT, padx=20)

        if materias:
            ttk.Label(frame, text="Materias más frecuentes:", font=('Arial', 12)).pack(pady=10, anchor='w')

            for materia, cant in sorted(materias.items(), key=lambda x: x[1], reverse=True)[:5]:
                ttk.Label(frame, text=f"- {materia}: {cant} estudiantes", font=('Arial', 10)).pack(anchor='w', padx=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = VistaListaApp(root)
    root.mainloop()