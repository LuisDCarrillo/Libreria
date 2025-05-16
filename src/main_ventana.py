import tkinter as tk
import subprocess
import os

# Funciones para los botones
def abrir_listas():
    subprocess.run(["python", "src/vista_lista.py"])

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

# Centrar la ventana en la pantalla
def centrar_ventana():
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

# Crear frame para centrar los botones
frame_centro = tk.Frame(ventana)
frame_centro.place(relx=0.5, rely=0.5, anchor="center")

# Crear botones
btn_listas = tk.Button(frame_centro, text="Listas", command=abrir_listas)
btn_colas = tk.Button(frame_centro, text="Colas", command=abrir_colas)

# Ubicar botones en el frame
btn_listas.pack(pady=10)
btn_colas.pack(pady=10)

# Centrar la ventana
centrar_ventana()

# Vincular la función al evento de cierre de la ventana principal
ventana.protocol("WM_DELETE_WINDOW", lambda: (borrar_datos_estudiantes(), ventana.destroy()))

# Ejecutar ventana principal
ventana.mainloop()