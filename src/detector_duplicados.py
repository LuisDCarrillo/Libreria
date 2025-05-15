import tkinter as messagebox
from tkinter import messagebox

def detectar_duplicados(lista_ingresados, lista_no_ingresados, root):
    duplicados = {}
    revisados = set()

    for lista in [lista_ingresados, lista_no_ingresados]:
        p = lista.Primero
        while p:
            cedula = p.info.cedula
            if cedula in revisados:
                duplicados.setdefault(cedula, []).append(p.info)
            else:
                revisados.add(cedula)
            p = p.prox

    if not duplicados:
        messagebox.showinfo("Duplicados", "No se encontraron estudiantes duplicados.")
        return
    
    for cedula, estudiantes in duplicados.items():
            estudiantes_str = "\n".join([f"{estudiante.cedula} - {estudiante.nombre}" for estudiante in estudiantes])
            messagebox.showinfo("Duplicados", f"Estudiantes duplicados con la cédula {cedula}:\n{estudiantes_str}")

  