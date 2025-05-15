import tkinter as tk
import subprocess
import os
from vista_pilas import InscripcionesApp

# Funciones para los botones
def abrir_listas():
    subprocess.run(["python", "src/vista_lista.py"])

def abrir_pilas():
    ventana_pilas = tk.Tk()
    app = InscripcionesApp(ventana_pilas)
    ventana_pilas.mainloop()

def abrir_colas():
    subprocess.run(["python", "src/vista_colas.py"])

# Función para borrar los datos de estudiantes inscritos
def borrar_datos_estudiantes():
    temp_file = "temp_estudiantes.json"
    if os.path.exists(temp_file):
        os.remove(temp_file)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Ventana con Botones")
ventana.geometry("300x200")

# Crear botones
btn_listas = tk.Button(ventana, text="Listas", command=abrir_listas)
btn_pilas = tk.Button(ventana, text="Pilas", command=abrir_pilas)
btn_colas = tk.Button(ventana, text="Colas", command=abrir_colas)

# Ubicar botones en la ventana
btn_listas.pack(pady=10)
btn_pilas.pack(pady=10)
btn_colas.pack(pady=10)

# Vincular la función al evento de cierre de la ventana principal
ventana.protocol("WM_DELETE_WINDOW", lambda: (borrar_datos_estudiantes(), ventana.destroy()))

# Ejecutar ventana principal
ventana.mainloop()