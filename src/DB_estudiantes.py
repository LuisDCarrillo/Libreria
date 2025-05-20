from Lista import Lista
from Estudiante import Estudiante

class DBEstudiantes:

    def guardar(self, lista: Lista):
        
        estudiantes = []
        
        for item in lista.obtener_todos():
            info = item.getInfo()
            info[3] = ". ".join(info[3])
            estudiantes.append(",".join(info))
        
        with open("estudiantes.txt", "w", encoding="utf-8") as archivo:
            for estudiante in estudiantes:
                archivo.write(estudiante + "\n")

    def Leer(self):
        lista = Lista()
        
        with open("estudiantes.txt", "r", encoding="utf-8") as archivo:
            estudiantes_leidos = [linea.strip() for linea in archivo]
            if estudiantes_leidos:
                for index, estudiante in enumerate(estudiantes_leidos):
                    estudiantes_leidos[index] = estudiantes_leidos[index].split(",")

                    if lista.Vacia():
                        lista.InsComienzo(Estudiante(estudiantes_leidos[index][0],estudiantes_leidos[index][1],estudiantes_leidos[index][2],estudiantes_leidos[index][3].split(". "),estudiantes_leidos[index][4]))
                    else:
                        ultimo_nodo = lista.Primero
                        while ultimo_nodo.prox is not None:
                            ultimo_nodo = ultimo_nodo.prox
                        lista.InsDespues(ultimo_nodo, Estudiante(estudiantes_leidos[index][0],estudiantes_leidos[index][1],estudiantes_leidos[index][2],estudiantes_leidos[index][3].split(". "),estudiantes_leidos[index][4]))
        
        return lista;

