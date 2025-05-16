import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
import time

class vistaRA:
    def __init__(self, root, vista_lista):
        self.root = root
        self.root.title("Resumen Académico")
        self.root.geometry("600x800")

        self.vista_lista = vista_lista

        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=20)

        self.frameCarreras = ttk.Frame(self.frame)
        self.frameCarreras.pack(pady=10, fill="both", expand=True)

        self.frameMaterias = ttk.Frame(self.frame)
        self.frameMaterias.pack(pady=10)

        self.variablesM = []
        self.variablesC = []
        
        self.numColumnasM = 2
        self.filaM, self.columnaM = 1, 0

        self.numColumnasC = 2
        self.filaC, self.columnaC = 1, 0

        self.select_all_materias = ttk.Button(self.frameMaterias, text="Seleccionar Todas las Materias", command=self.seleccionarTodoM)
        self.select_all_carreras = ttk.Button(self.frameCarreras, text="Seleccionar Todas las Carreras", command=self.seleccionarTodoC)
        self.btn_resumen = ttk.Button(self.frame, text="Generar Resumen", command=self.generar_pdf)
        self.btn_salir = ttk.Button(self.frame, text="Salir", command=self.salir)

        self.estado_btn_resumen()
        self.checkbuttons_carreras()
        self.checkbuttons_materias()
        self.btn_salir.pack(pady=10)

    def obtener_materias(self):
        materias = set()
        m = self.vista_lista.lista_ingresados.Primero
        while m:
            estudiante = m.info
            if hasattr(estudiante, 'materias'): 
                for materia in estudiante.materias: 
                    materias.add(materia.strip())  
            m = m.prox

        m = self.vista_lista.lista_no_ingresados.Primero
        while m:
            estudiante = m.info
            if hasattr(estudiante, 'materias'): 
                for materia in estudiante.materias:
                    materias.add(materia.strip())  
            m = m.prox

        return sorted(materias)

    def checkbuttons_materias(self):

        materias = self.obtener_materias()

        if not materias:
            self.select_all_materias.pack_forget()

        else:
            self.labelMaterias = tk.Label(self.frameMaterias, text="Selecciona las materias que deseas incluir en el resumen")
            self.labelMaterias.grid(row=0, column=0, columnspan=2, pady=10)

            for materia in materias:
                var = tk.IntVar(value=0)
                self.variablesM.append(var)
                checkbox = tk.Checkbutton(self.frameMaterias, text=materia, variable=var, command=self.actualizar_estado_boton_materias)
                checkbox.grid(row=self.filaM, column=self.columnaM, sticky="w", padx=10, pady=2)
                self.columnaM += 1
                if self.columnaM >= self.numColumnasM:
                    self.columnaM = 0
                    self.filaM += 1
                self.select_all_materias.grid(row=self.filaM+1, column=0, columnspan=2, pady=10)

    def obtener_carreras(self):
        carreras = set()

        p = self.vista_lista.lista_ingresados.Primero
        while p:
            estudiante = p.info
            if hasattr(estudiante, 'carrera'): 
                carreras.add(estudiante.carrera.strip())
            p = p.prox

        p = self.vista_lista.lista_no_ingresados.Primero
        while p:
            estudiante = p.info
            if hasattr(estudiante, 'carrera'):
                carreras.add(estudiante.carrera.strip())
            p = p.prox

        return sorted(carreras)

    def checkbuttons_carreras(self):

        carreras = self.obtener_carreras()

        if not carreras:
            self.select_all_carreras.pack_forget()
            self.labelCarreras = tk.Label(self.frameCarreras, text="No hay estudiantes registrados")
            self.labelCarreras.grid(row=0, column=0, columnspan=2, pady=10)
        else:
            self.labelCarreras = tk.Label(self.frameCarreras, text="Selecciona las carreras que deseas incluir en el resumen")
            self.labelCarreras.grid(row=0, column=0, columnspan=2, pady=10)

        for carrera in carreras:
            var = tk.IntVar(value=0)
            self.variablesC.append(var)
            checkbox = tk.Checkbutton(self.frameCarreras, text=carrera, variable=var, command=self.actualizar_estado_boton_carreras)
            checkbox.grid(row=self.filaC, column=self.columnaC, sticky="w", padx=10, pady=2)
            self.columnaC += 1 
            if self.columnaC >= self.numColumnasC:
                self.columnaC = 0
                self.filaC += 1
            self.select_all_carreras.grid(row=self.filaC+1, column=0, columnspan=2, pady=10)

    def actualizar_estado_boton_materias(self):

        if all(var.get() == 1 for var in self.variablesM):
            self.select_all_materias.config(text="Deseleccionar Todas las Materias")
        else:
            self.select_all_materias.config(text="Seleccionar Todas las Materias")
    
    def actualizar_estado_boton_carreras(self):

        if all(var.get() == 1 for var in self.variablesC):
            self.select_all_carreras.config(text="Deseleccionar Todas las Carreras")
        else: 
            self.select_all_carreras.config(text="Seleccionar Todas las Carreras")

    def seleccionarTodoM(self):
        if all(var.get() == 0 for var in self.variablesM):
            for var in self.variablesM:
                var.set(1)
        else:
            for var in self.variablesM:
                var.set(0)
    
        self.actualizar_estado_boton_materias()

    def seleccionarTodoC(self):
        if all(var.get() == 0 for var in self.variablesC):
            for var in self.variablesC:
                var.set(1)
        else:
            for var in self.variablesC:
                var.set(0)
    
        self.actualizar_estado_boton_carreras()
    
    def salir(self):
        self.root.destroy()

    def estado_btn_resumen(self):

        tiene_estudiantes = self.vista_lista.lista_ingresados.Primero or self.vista_lista.lista_no_ingresados.Primero

        if tiene_estudiantes:
            self.btn_resumen.pack(pady=10)
        else:
            self.btn_resumen.pack_forget()

    def limpiar_checkbuttons(self):
        for var in self.variablesM:
            var.set(0) 
        for var in self.variablesC:
            var.set(0)
            self.actualizar_estado_boton_materias()
            self.actualizar_estado_boton_carreras()

    def generar_pdf(self):

        estilos = getSampleStyleSheet()  
        estudiantes_filtrados = []

        materias_seleccionadas = [materia for var, materia in zip(self.variablesM, self.obtener_materias()) if var.get() == 1]
        carreras_seleccionadas = [carrera for var, carrera in zip(self.variablesC, self.obtener_carreras()) if var.get() == 1]

        if not materias_seleccionadas and not carreras_seleccionadas:
            messagebox.showinfo("PDF", "No has seleccionado ninguna materia o carrera.")
            return

        carpeta_documentos = os.path.expanduser("~/Documents")  
        archivo_pdf = os.path.join(carpeta_documentos, f"Resumen Académico_{int(time.time())}.pdf")

        nodo = self.vista_lista.lista_ingresados.Primero
        while nodo:
            estudiante = nodo.info

            filtro_materia = any(materia in estudiante.materias for materia in materias_seleccionadas) if materias_seleccionadas else True
            filtro_carrera = estudiante.carrera in carreras_seleccionadas if carreras_seleccionadas else True

            if filtro_materia and filtro_carrera:
                estudiantes_filtrados.append([
                    Paragraph(str(estudiante.cedula), estilos["Normal"]),
                    Paragraph(estudiante.nombre, estilos["Normal"]),
                    Paragraph(str(estudiante.carrera), estilos["Normal"]),
                    Paragraph(str(estudiante.uc_aprobadas), estilos["Normal"]),
                    Paragraph(", ".join(estudiante.materias), estilos["Normal"])
                ])
                
            nodo = nodo.prox  

        nodo = self.vista_lista.lista_no_ingresados.Primero
        while nodo:
            estudiante = nodo.info

            filtro_materia = any(materia in estudiante.materias for materia in materias_seleccionadas) if materias_seleccionadas else True
            filtro_carrera = estudiante.carrera in carreras_seleccionadas if carreras_seleccionadas else True

            if filtro_materia and filtro_carrera:
                estudiantes_filtrados.append([
                    Paragraph(str(estudiante.cedula), estilos["Normal"]),
                    Paragraph(estudiante.nombre, estilos["Normal"]),
                    Paragraph(str(estudiante.carrera), estilos["Normal"]),
                    Paragraph(str(estudiante.uc_aprobadas), estilos["Normal"]),
                    Paragraph(", ".join(estudiante.materias), estilos["Normal"])
                ])

            nodo = nodo.prox  

        if not estudiantes_filtrados:
            messagebox.showinfo("PDF", "No hay estudiantes que coincidan con los criterios seleccionados.")
            return

        doc = SimpleDocTemplate(archivo_pdf, pagesize=letter)
        elementos = []

        encabezados = [
            Paragraph("Cedula", estilos["Heading3"]),
            Paragraph("Nombre", estilos["Heading3"]),
            Paragraph("Carrera", estilos["Heading3"]),
            Paragraph("Materias", estilos["Heading3"]),
            Paragraph("UC Aprobadas", estilos["Heading3"])
        ]
        
        tabla = Table([encabezados] + estudiantes_filtrados)

        estilo = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        tabla.setStyle(estilo)

        elementos.append(tabla)
        doc.build(elementos)
        self.limpiar_checkbuttons()

        messagebox.showinfo("PDF", f"El resumen se ha generado correctamente en: {archivo_pdf}")

if __name__ == "__main__":
    root = tk.Tk()
    vista = vistaRA(root)
    root.mainloop()