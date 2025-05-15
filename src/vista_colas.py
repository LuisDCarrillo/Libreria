import tkinter as tk
from tkinter import messagebox
from Colas import Cola
from EstudianteC import Estudiante

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Visualización de Cola")
ventana.geometry("800x500")
ventana.resizable(0,0) # Impidiendo redimensión de la ventana

# Crear una instancia de Cola
cola = Cola()

# Función para dibujar la cola
def dibujar_cola():
    canvas.delete("all")  # Limpiar el canvas antes de redibujar

    if cola.Vacia():
        canvas.create_text(375, 40, text="[Espacio en memoria]", font=("Arial", 14))
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
    mensaje = f"El estudiante esta siendo atendido:\n" \
                f"Cédula: {estudiante.cedula}\n" \
                f"Nombre: {estudiante.nombre}\n" \
                f"Razón: {razon}"
    anuncio.config(text=mensaje, fg="black")

# Función para insertar un elemento en la cola
def insertar():
    if not cola_cabe_en_canvas():
        messagebox.showwarning("Error", "¡La cola está llena (memoria llena)!")
        canvas.create_text(375, 80, text="[Cola llena (memoria llena)]", font=("Arial", 14))
        return
    
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
    entry_prioridad.delete(0, tk.END)

# Remover elemento de la cola
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

def ordenar_prioridad():
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
#Creando el frame para el canvas
frame_canvas = tk.Frame(ventana)
frame_canvas.pack(side=tk.TOP)

# Creando scrollbar para el canvas
scrollbar_horizontal = tk.Scrollbar(frame_canvas, orient=tk.HORIZONTAL)
scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

# Canvas para dibujar la cola
canvas = tk.Canvas(frame_canvas, width=750, height=250, bg="white", xscrollcommand=scrollbar_horizontal.set)
canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
scrollbar_horizontal.config(command=canvas.xview)

# Etiqueta para mostrar el anuncio del estudiante siendo atendido
anuncio = tk.Label(ventana, text="No hay estudiantes en la cola",
font=("Arial", 12), fg="black", justify=tk.LEFT, highlightthickness=1, highlightbackground="black")
anuncio.place(relx=0.8, rely=0.7, anchor="e")

# Creando un frame (contenedor) para los botones y entradas
# y organizando su disposición
frame_botones = tk.Frame(ventana)
frame_botones.pack(side=tk.BOTTOM, pady=10)
frame_botones.config(cursor="hand2") # Modificando el cursor de los botones
frame_entrada = tk.Frame(ventana)
frame_entrada.pack(anchor="w", padx=10)

# Creando los botones y entradas de texto
label_txt_entrada = tk.Label(frame_entrada, text="Inserte los datos necesarios\npara visualizar:", justify=tk.LEFT)
label_txt_entrada.pack(anchor="w")
frame_cedula = tk.Frame(frame_entrada)
frame_cedula.pack(anchor="w")
label_txt_cedula = tk.Label(frame_cedula, text="Cédula:", width=7, anchor="w")
label_txt_cedula.pack(side=tk.LEFT)
entry_cedula = tk.Entry(frame_cedula)
entry_cedula.pack(side=tk.LEFT, padx=5)

frame_nombre = tk.Frame(frame_entrada)
frame_nombre.pack(anchor="w")
label_txt_nombre = tk.Label(frame_nombre, text="Nombre:", width=7, anchor="w")
label_txt_nombre.pack(side=tk.LEFT)
entry_nombre = tk.Entry(frame_nombre)
entry_nombre.pack(side=tk.LEFT, padx=5)

frame_edad = tk.Frame(frame_entrada)
frame_edad.pack(anchor="w")
label_txt_edad = tk.Label(frame_edad, text="Edad:", width=7, anchor="w")
label_txt_edad.pack(side=tk.LEFT)
entry_edad = tk.Entry(frame_edad)
entry_edad.pack(side=tk.LEFT, padx=5)

frame_carrera = tk.Frame(frame_entrada)
frame_carrera.pack(anchor="w")
label_txt_carrera = tk.Label(frame_carrera, text="Carrera:" , width=7, anchor="w")
label_txt_carrera.pack(side=tk.LEFT)
entry_carrera = tk.Entry(frame_carrera)
entry_carrera.pack(side=tk.LEFT , padx=5)

frame_razon = tk.Frame(frame_entrada)
frame_razon.pack(anchor="w")
label_txt_razon = tk.Label(frame_razon, text="Razón:", width=7, anchor="w")
label_txt_razon.pack(side=tk.LEFT)
entry_razon = tk.Entry(frame_razon)
entry_razon.pack(side=tk.LEFT , padx=5)

frame_prioridad = tk.Frame(frame_entrada)
frame_prioridad.pack(anchor="w")
label_txt_prioridad = tk.Label(frame_prioridad, text="Prioridad:", width=7, anchor="w")
label_txt_prioridad.pack(side=tk.LEFT)
entry_prioridad = tk.Entry(frame_prioridad)
entry_prioridad.pack(side=tk.LEFT , padx=5)

btn_insertar = tk.Button(frame_botones, text="Insertar", command=insertar)
btn_insertar.pack(side=tk.LEFT, padx=5)

btn_remover = tk.Button(frame_botones, text="Remover", command=remover)
btn_remover.pack(side=tk.LEFT, padx=5)

btn_ordenar = tk.Button(frame_botones, text="Ordenar por prioridad", command=ordenar_prioridad)
btn_ordenar.pack(side=tk.LEFT, padx=5)

# Mostrar cola inicial
dibujar_cola()
ventana.mainloop()