import tkinter as tk
from tkinter import ttk, messagebox
from Pila import Pila, NodoPila

# Supongamos que este es el diccionario de créditos por materia
MATERIAS_CREDITOS = {
    "Matemáticas": 4,
    "Física": 4,
    "Programación": 3,
    "Historia": 3
}

class InscripcionesApp:
    def __init__(self, root, estudiante=None, on_close=None, materias_creditos=None):
        self.root = root
        self.on_close = on_close
        self.estudiante = estudiante
        self.materias_creditos = materias_creditos or {}

        if estudiante:
            # Cargar materias del estudiante
            materias = estudiante.materias if isinstance(estudiante.materias, list) else estudiante.materias.split(',')
            self.pila = Pila()
            for materia in materias:
                if materia.strip():
                    self.pila.Insertar(materia.strip())
        else:
            self.pila = Pila()

        self.materias = list(self.materias_creditos.keys())
        self.configurar_interfaz()
        self.crear_widgets()
        if estudiante:
            self.actualizar_interfaz()
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def configurar_interfaz(self):
        self.root.title("Gestión de Inscripciones")
        self.root.geometry("800x650")
        self.root.configure(bg='#f0f0f0')

    def crear_widgets(self):
        # Frame principal
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Información del estudiante
        self.label_estudiante = ttk.Label(self.frame_principal, text="Estudiante: No seleccionado", font=("Arial", 12))
        self.label_estudiante.pack(pady=5)

        # Información de créditos
        self.label_creditos = ttk.Label(self.frame_principal, text="Créditos Totales: 0 / 16", font=("Arial", 10))
        self.label_creditos.pack(pady=5)

        # Selección de materia
        self.frame_seleccion = ttk.LabelFrame(self.frame_principal, text="Inscripción de Materias Disponibles")
        self.frame_seleccion.pack(fill=tk.X, pady=10)

        # Actualizar el combobox con las materias de materias_creditos
        self.combo_materias = ttk.Combobox(
            self.frame_seleccion,
            values=self.materias,
            state="readonly"
        )
        self.combo_materias.pack(side=tk.LEFT, padx=5, pady=5)
        self.combo_materias.bind("<<ComboboxSelected>>", self.habilitar_boton_inscribir) # Habilitar al seleccionar

        self.btn_inscribir = ttk.Button(
            self.frame_seleccion,
            text="Inscribir",
            command=self.inscribir_materia,
            state=tk.DISABLED # Inicialmente deshabilitado
        )
        self.btn_inscribir.pack(side=tk.LEFT, padx=5)

        # Acciones
        self.frame_acciones = ttk.Frame(self.frame_principal)
        self.frame_acciones.pack(fill=tk.X, pady=10)

        self.btn_desinscribir = ttk.Button(
            self.frame_acciones,
            text="Desinscribir Última Materia",
            command=self.confirmar_desinscripcion
        )
        self.btn_desinscribir.pack(side=tk.LEFT, padx=5)

        # Historial
        self.frame_historial = ttk.LabelFrame(self.frame_principal, text="Materias Inscritas")
        self.frame_historial.pack(fill=tk.BOTH, expand=True)

        self.lista_materias = tk.Listbox(
            self.frame_historial,
            height=10,
            font=('Arial', 10)
        )
        self.lista_materias.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Representación gráfica
        self.frame_pila = ttk.LabelFrame(self.frame_principal, text="Estructura de Pila")
        self.frame_pila.pack(fill=tk.X, pady=10)

        self.canvas = tk.Canvas(
            self.frame_pila,
            bg='white',
            height=150,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.X, padx=5, pady=5)

    def habilitar_boton_inscribir(self, event):
        self.btn_inscribir.config(state=tk.NORMAL)

    def calcular_creditos_totales(self):
        creditos = 0
        for materia in self.pila.obtener_contenido():
            if materia in self.materias_creditos:
                creditos += self.materias_creditos[materia]
        return creditos

    def inscribir_materia(self):
        materia = self.combo_materias.get()

        if not materia:
            messagebox.showwarning("Error", "Seleccione una materia")
            return

        # Verificar si la materia ya está inscrita
        if self.materia_ya_inscrita(materia):
            messagebox.showwarning("Error", f"Ya está inscrito en {materia}")
            return

        # Validar restricciones de inscripción
        creditos_actuales = self.calcular_creditos_totales()
        if materia in self.materias_creditos and (creditos_actuales + self.materias_creditos[materia] > 16):
            messagebox.showerror("Error de Créditos", "No se puede inscribir porque excede el límite de créditos.")
            return

        # Insertar la materia en la pila
        if self.pila.Insertar(materia):
            self.actualizar_interfaz()
            messagebox.showinfo("Éxito", f"Inscrito en {materia}")
            self.combo_materias.set("") # Limpiar la selección después de inscribir
            self.btn_inscribir.config(state=tk.DISABLED) # Deshabilitar de nuevo

            # Actualizar la vista de lista
            if self.on_close and self.estudiante:
                materias_actuales = list(reversed(self.pila.obtener_contenido()))
                self.estudiante.materias = materias_actuales
                self.on_close(self.estudiante)
        else:
            messagebox.showerror("Error", "No se pudo inscribir (memoria llena)")

    def confirmar_desinscripcion(self):
        if not self.pila.Vacia():
            materia_top_nodo = self.pila.ObtTope()
            if materia_top_nodo:
                materia_top = materia_top_nodo.info
                confirmacion = messagebox.askyesno(
                    "Confirmar Desinscripción",
                    f"¿Seguro que desea desinscribir la última materia inscrita: {materia_top}?"
                )
                if confirmacion:
                    self.desinscribir_materia()
            else:
                messagebox.showwarning("Error", "No se pudo obtener la materia del tope.")
        else:
            messagebox.showwarning("Error", "No hay materias inscritas para desinscribir.")

    def desinscribir_materia(self):
        # Remover la última materia inscrita
        materia = self.pila.Remover()
        if materia:
            self.actualizar_interfaz()
            messagebox.showinfo("Desinscrito", f"Se eliminó: {materia}")
            if self.on_close and self.estudiante:
                materias_actuales = list(reversed(self.pila.obtener_contenido()))
                self.estudiante.materias = materias_actuales
                self.on_close(self.estudiante)
        else:
            messagebox.showwarning("Error", "No hay materias inscritas")

    def materia_ya_inscrita(self, materia):
        return materia in self.pila.obtener_contenido()

    def actualizar_interfaz(self):
        # Mostrar información del estudiante
        if self.estudiante:
            self.label_estudiante.config(text=f"Estudiante: {self.estudiante.nombre} ({self.estudiante.cedula})")
        # Actualizar lista de materias con créditos
        self.lista_materias.delete(0, tk.END)
        for materia in reversed(self.pila.obtener_contenido()):
            creditos = self.materias_creditos.get(materia, "N/A")
            self.lista_materias.insert(tk.END, f"{materia} ({creditos} créditos)")
        # Dibujar pila
        self.dibujar_pila()
        # Actualizar la etiqueta de créditos
        creditos_totales = self.calcular_creditos_totales()
        self.label_creditos.config(text=f"Créditos Totales: {creditos_totales} / 16")

    def dibujar_pila(self):
        self.canvas.delete("all")
        contenido = self.pila.obtener_contenido()

        if not contenido:
            self.canvas.create_text(150, 75, text="Pila vacía", font=('Arial', 12))
            return

        ancho = self.canvas.winfo_width()
        x = ancho // 2
        y = 20
        ancho_rect = 200
        alto_rect = 30

        for i, materia in enumerate(contenido):
            color = "#E3F2FD" if i % 2 == 0 else "#BBDEFB"

            # Rectángulo
            self.canvas.create_rectangle(
                x - ancho_rect//2, y,
                x + ancho_rect//2, y + alto_rect,
                fill=color, outline="#1976D2"
            )

            # Texto
            self.canvas.create_text(
                x, y + alto_rect//2,
                text=materia,
                font=('Arial', 9)
            )

            # Indicador TOP
            if i == 0:
                self.canvas.create_text(
                    x + ancho_rect//2 - 15, y + 5,
                    text="TOP",
                    font=('Arial', 7, 'bold'),
                    fill="#D32F2F"
                )

            y += alto_rect + 5

    def cerrar_ventana(self):
        # Actualizar las materias del estudiante al cerrar la ventana
        if self.on_close and self.estudiante:
            materias_actuales = list(reversed(self.pila.obtener_contenido()))
            creditos_totales = self.calcular_creditos_totales()

            if creditos_totales > 16:
                messagebox.showerror("Error de Créditos", "No se puede guardar porque excede el límite de créditos.")
                return

            self.estudiante.materias = materias_actuales
            self.on_close(self.estudiante)
        self.root.destroy()

def main():
    root = tk.Tk()
    app = InscripcionesApp(root, materias_creditos=MATERIAS_CREDITOS)
    root.mainloop()

if __name__ == "__main__":
    main()