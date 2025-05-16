import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Colas import Cola
from EstudianteC import Estudiante

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Visualización de Cola - Estudiantes")
ventana.geometry("800x550")
ventana.resizable(0, 0)
ventana.configure(bg="#CCD1D1")  # Fondo gris claro

# Configurar estilos para los widgets ttk
estilo = ttk.Style()
estilo.theme_use('clam')

# Estilo para los botones
estilo.configure('TButton', 
               font=('Arial', 10, 'bold'),
               background="#AED6F1",  # Azul claro
               foreground="black",
               padding=10,
               borderwidth=1)

# Efecto al pasar el mouse sobre los botones
estilo.map('TButton',
          background=[('active', "#1E3F66")],  # Azul oscuro
          foreground=[('active', 'white')])

# Crear una instancia de Cola
cola = Cola()

# Función para dibujar la cola en el canvas
def dibujar_cola():
    canvas.delete("all")  # Limpiar el canvas antes de redibujar

    if cola.Vacia():
        canvas.create_text(375, 80, text="[La cola está vacía]", font=("Arial", 14))
        canvas.create_rectangle(320, 130, 430, 190, fill="lightblue")
        canvas.create_line(410, 130, 410, 190, fill="black")
        anuncio.config(text="No hay estudiantes en la cola", fg="black")
        return

    x = 100  # Posición inicial en X
    y = 150  # Posición fija en Y
    separacion = 130  # Espacio entre nodos

    p = cola.Frente
    while p is not None:
        canvas.create_text(375, 40, text="[Espacio en memoria]", font=("Arial", 14))
        # Dibujar nodo (círculo + texto)
        canvas.create_rectangle(x, y-30, x+110, y+30, fill="lightblue")
        canvas.create_text(x+45, y, text=str(p.info.cedula), font=("Arial", 12))
        canvas.create_line(x+90, y-30, x+90, y+30, fill="black")  # Línea vertical

        # Dibujar flecha si hay un nodo siguiente
        if p.prox is not None:
            canvas.create_line(x+110, y, x+separacion, y, arrow=tk.LAST)

        # Resaltar Frente (rojo) y Final (verde)
        if p == cola.Frente:
            canvas.create_text(x+40, y-50, text="Frente", fill="red", font=("Arial", 10, "bold"))
            mostrar_estudiante_atendido(p.info)
        if p == cola.Final:
            canvas.create_text(x+40, y+50, text="Final", fill="green", font=("Arial", 10, "bold"))
            canvas.create_line(x+110, y-30, x+90, y+30, fill="black")

        x += separacion
        p = p.prox
        canvas.config(scrollregion=canvas.bbox("all"))

# Función para mostrar información del estudiante siendo atendido
def mostrar_estudiante_atendido(estudiante):
    razon = estudiante.describir_razon()
    mensaje = f"Estudiante siendo atendido:\n" \
             f"Cédula: {estudiante.cedula}\n" \
             f"Nombre: {estudiante.nombre}\n" \
             f"Razón: {razon}\n" \
             f"Prioridad: {estudiante.prioridad}"
    anuncio.config(text=mensaje, fg="black")

# Función para insertar un estudiante en la cola
def insertar():
    if not cola_cabe_en_canvas():
        messagebox.showwarning("Error", "¡La cola está llena (memoria llena)!")
        canvas.create_text(375, 80, text="[Cola llena (memoria llena)]", font=("Arial", 14))
        return

    try:
        # Validar prioridad (1-5)
        prioridad = int(entry_prioridad.get())
        if not (1 <= prioridad <= 5):
            messagebox.showerror("Error", "La prioridad debe estar entre 1 y 5")
            return
        
        # Validar razón (1-3)
        razon = int(entry_razon.get())
        if not (1 <= razon <= 3):
            messagebox.showerror("Error", "La razón debe estar entre 1 y 3")
            return
            
    except ValueError:
        messagebox.showerror("Error", "Prioridad y razón deben ser números enteros")
        return
    
    # Obtener datos de los campos de entrada
    cedula = entry_cedula.get()
    nombre = entry_nombre.get()
    edad = entry_edad.get()
    carrera = entry_carrera.get()
    razon = entry_razon.get()
    prioridad = int(entry_prioridad.get())
    
    if (cedula and nombre and edad and carrera and razon and prioridad):
        estudiante = Estudiante(cedula, nombre, edad, carrera, razon, prioridad)
        if cola.Insertar(estudiante):
            dibujar_cola()
            estudiante.mostrar_informacion()
            estudiante.describir_razon()
            messagebox.showinfo("Info", "Estudiante agregado a la cola.")
            cola.MostrarContenido()
        else:
            messagebox.showerror("Error", "¡La cola está llena (memoria llena)!")
    else:
        messagebox.showwarning("Advertencia", "Ingresa un valor.")
    limpiar_entradas()
    # Limpiar entradas de texto después de insertar

# Limpiar entradas de texto después de insertar
def limpiar_entradas():
    entry_cedula.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    entry_carrera.delete(0, tk.END)
    entry_razon.delete(0, tk.END)
    if hasattr(entry_prioridad, 'delete'):
        entry_prioridad.delete(0, tk.END)

# Función para remover un estudiante de la cola
def remover():
    if cola.Vacia():
        messagebox.showinfo("Info", "La cola está vacía.")
    else:
        estudiante_removido = cola.Remover()
        if estudiante_removido:
            messagebox.showinfo("Info", f"Se atendió al estudiante: {estudiante_removido.cedula}")
        dibujar_cola()
        
# Método para contar cantidad de nodos y calcula si hay espacio para uno más
def cola_cabe_en_canvas():
    longitud_cola = 0
    nodo = cola.Frente
    while nodo:
        longitud_cola += 1
        nodo = nodo.prox
    
    separacion = 130  # Igual que en dibujar_cola()
    espacio_necesario = separacion * (longitud_cola + 1)
    ancho_canvas = canvas.winfo_width()

    return espacio_necesario <= ancho_canvas

def ordenar_por_prioridad():
    global cola
    cola_aux = Cola()
    i = 1
    while i < 11:
        p = cola.Frente
        while p is not None:
            if (p.info.prioridad == i):
                cola_aux.Insertar(p.info)
            p = p.prox
        i += 1
    cola_aux.MostrarContenido()
    cola = cola_aux
    dibujar_cola()

# Frame para el canvas y scrollbar
frame_canvas = tk.Frame(ventana, bg="#CCD1D1")
frame_canvas.pack(side=tk.TOP)

scrollbar_horizontal = tk.Scrollbar(frame_canvas, orient=tk.HORIZONTAL)
scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

# Canvas para dibujar la cola
canvas = tk.Canvas(frame_canvas, width=750, height=250, bg="#CCD1D1", xscrollcommand=scrollbar_horizontal.set)
canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
scrollbar_horizontal.config(command=canvas.xview)

# Etiqueta para mostrar información del estudiante atendido
anuncio = tk.Label(ventana, text="No hay estudiantes en la cola",
                  font=("Arial", 12), fg="black", justify=tk.LEFT, 
                  bg="#CCD1D1", wraplength=500)
anuncio.place(relx=0.8, rely=0.7, anchor="e")

# Frame para los campos de entrada
frame_entrada = tk.Frame(ventana, bg="#CCD1D1")
frame_entrada.pack(anchor="w", padx=20, pady=10)

# Título de la sección de entrada
label_titulo = tk.Label(frame_entrada, text="Inserte los datos necesarios para visualizar: ", 
                       font=("Arial", 11, "bold"), bg="#CCD1D1")
label_titulo.pack(anchor="w", pady=5)

# Campos de entrada
campos = [
    ("Cédula", "entry_cedula"),
    ("Nombre", "entry_nombre"),
    ("Edad", "entry_edad"),
    ("Carrera", "entry_carrera"),
    ("Razón (1-3)", "entry_razon"),
    ("Prioridad (1-5)", "entry_prioridad")  # Nuevo campo
]

for texto, var_name in campos:
    frame = tk.Frame(frame_entrada, bg="#CCD1D1")
    frame.pack(fill=tk.X, pady=2)
    
    label = tk.Label(frame, text=f"{texto}:", width=15, anchor="w", bg="#CCD1D1")
    label.pack(side=tk.LEFT)
    
    entry = ttk.Entry(frame, font=("Arial", 11))
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Guardar referencia a los campos
    globals()[var_name] = entry

# Frame para los botones
frame_botones = tk.Frame(ventana, bg="#CCD1D1")
frame_botones.pack(fill=tk.X, padx=20, pady=10)
frame_botones.config(cursor="hand2") # Modificando el cursor de los botones
frame_entrada = tk.Frame(ventana)
frame_entrada.pack(anchor="w", padx=10)

# Configurar columnas para los botones
frame_botones.columnconfigure(0, weight=1)
frame_botones.columnconfigure(1, weight=1)
frame_botones.columnconfigure(2, weight=1)
frame_botones.columnconfigure(3, weight=1)

# Botones con estilo ttk
btn_insertar = ttk.Button(frame_botones, text="INSERTAR ESTUDIANTE", command=insertar)
btn_insertar.grid(row=0, column=0, padx=5, sticky="ew")

btn_ordenar = ttk.Button(frame_botones, text="ORDENAR POR PRIORIDAD", command=ordenar_por_prioridad)
btn_ordenar.grid(row=0, column=1, padx=5, sticky="ew")

btn_remover = ttk.Button(frame_botones, text="REMOVER ESTUDIANTE", command=remover)
btn_remover.grid(row=0, column=2, padx=5, sticky="ew")

btn_limpiar = ttk.Button(frame_botones, text="LIMPIAR CAMPOS", command=limpiar_entradas)
btn_limpiar.grid(row=0, column=3, padx=5, sticky="ew")

# Mostrar cola inicial
dibujar_cola()
ventana.mainloop()