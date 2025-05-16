import tkinter as tk
from tkinter import messagebox
from Colas import Cola
from EstudianteC import Estudiante

class VistaColasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualización de Cola")
        self.root.geometry("800x600")

        # Inicializar la cola
        self.cola = Cola()
        
        # Frame principal
        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas para dibujar la cola
        self.canvas_frame = tk.Frame(self.frame_principal)
        self.canvas_frame.pack(fill="both", expand=True, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", height=300)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Scrollbar para el canvas
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame para los controles
        self.frame_controles = tk.Frame(self.frame_principal)
        self.frame_controles.pack(fill="x", pady=10)

        # Campos de entrada
        self.frame_campos = tk.Frame(self.frame_controles)
        self.frame_campos.pack(side="left", padx=10)
        
        tk.Label(self.frame_campos, text="Cédula:").grid(row=0, column=0, padx=5, pady=2)
        self.cedula_entry = tk.Entry(self.frame_campos)
        self.cedula_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(self.frame_campos, text="Nombre:").grid(row=1, column=0, padx=5, pady=2)
        self.nombre_entry = tk.Entry(self.frame_campos)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(self.frame_campos, text="Carrera:").grid(row=2, column=0, padx=5, pady=2)
        self.carrera_entry = tk.Entry(self.frame_campos)
        self.carrera_entry.grid(row=2, column=1, padx=5, pady=2)
        
        tk.Label(self.frame_campos, text="Materias:").grid(row=3, column=0, padx=5, pady=2)
        self.materias_entry = tk.Entry(self.frame_campos)
        self.materias_entry.grid(row=3, column=1, padx=5, pady=2)
        
        tk.Label(self.frame_campos, text="UC Aprobadas:").grid(row=4, column=0, padx=5, pady=2)
        self.uc_entry = tk.Entry(self.frame_campos)
        self.uc_entry.grid(row=4, column=1, padx=5, pady=2)

        # Frame para botones
        self.frame_botones = tk.Frame(self.frame_controles)
        self.frame_botones.pack(side="right", padx=10)
        
        tk.Button(self.frame_botones, text="Insertar", command=self.insertar).pack(side="left", padx=5)
        tk.Button(self.frame_botones, text="Remover", command=self.remover).pack(side="left", padx=5)
        tk.Button(self.frame_botones, text="Ordenar por Prioridad", command=self.ordenar_prioridad).pack(side="left", padx=5)

        # Dibujar la cola inicial
        self.dibujar_cola()

    def dibujar_cola(self):
        self.canvas.delete("all")
        if self.cola.Vacia():
            self.canvas.create_text(400, 150, text="[Cola vacía]", font=("Arial", 14))
            return

        x = 100
        y = 150
        separacion = 120

        p = self.cola.frente
        while p is not None:
            # Dibujar nodo
            self.canvas.create_rectangle(x - 50, y - 30, x + 50, y + 30, fill="lightblue")
            self.canvas.create_text(x, y, text=str(p.info.cedula), font=("Arial", 12))

            # Dibujar flecha si hay próximo nodo
            if p.prox is not None:
                self.canvas.create_line(x + 50, y, x + separacion - 30, y, arrow=tk.LAST)

            # Etiquetar frente y final
            if p == self.cola.frente:
                self.canvas.create_text(x, y - 50, text="Frente", fill="red", font=("Arial", 10, "bold"))
            if p == self.cola.final:
                self.canvas.create_text(x, y + 50, text="Final", fill="red", font=("Arial", 10, "bold"))

            x += separacion
            p = p.prox

    def insertar(self):
        try:
            cedula = self.cedula_entry.get().strip()
            nombre = self.nombre_entry.get().strip()
            carrera = self.carrera_entry.get().strip()
            materias = [m.strip() for m in self.materias_entry.get().split(",")]
            uc_aprobadas = self.uc_entry.get().strip()

            if not all([cedula, nombre, carrera, materias, uc_aprobadas]):
                messagebox.showwarning("Campos incompletos", "Todos los campos deben estar llenos.")
                return

            if not cedula.isdigit():
                messagebox.showerror("Error", "La cédula debe contener solo números.")
                return

            if not uc_aprobadas.isdigit():
                messagebox.showerror("Error", "Las UC aprobadas deben ser un número.")
                return

            estudiante = Estudiante(cedula, nombre, carrera, materias, uc_aprobadas)
            self.cola.Insertar(estudiante)
            self.dibujar_cola()
            self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar: {str(e)}")

    def remover(self):
        if self.cola.Vacia():
            messagebox.showinfo("Cola vacía", "No hay elementos para remover.")
            return

        estudiante = self.cola.Remover()
        messagebox.showinfo("Estudiante removido", f"Se removió el estudiante: {estudiante.nombre}")
        self.dibujar_cola()

    def ordenar_prioridad(self):
        if self.cola.Vacia():
            messagebox.showinfo("Cola vacía", "No hay elementos para ordenar.")
            return

        # Crear una cola temporal para ordenar
        cola_aux = Cola()
        
        # Mover todos los elementos a la cola temporal
        while not self.cola.Vacia():
            cola_aux.Insertar(self.cola.Remover())
        
        # Ordenar por UC aprobadas (mayor a menor)
        estudiantes = []
        while not cola_aux.Vacia():
            estudiantes.append(cola_aux.Remover())
        
        estudiantes.sort(key=lambda x: int(x.uc_aprobadas), reverse=True)
        
        # Reinsertar en orden
        for estudiante in estudiantes:
            self.cola.Insertar(estudiante)
        
        self.dibujar_cola()
        messagebox.showinfo("Ordenamiento", "Cola ordenada por UC aprobadas.")

    def limpiar_campos(self):
        self.cedula_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.carrera_entry.delete(0, tk.END)
        self.materias_entry.delete(0, tk.END)
        self.uc_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaColasApp(root)
    root.mainloop()