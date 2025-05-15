class Estudiante:
    def __init__(self, cedula, nombre, carrera, materias, uc_aprobadas):
        self.cedula = cedula
        self.nombre = nombre
        self.carrera = carrera
        self.materias = materias
        self.uc_aprobadas = uc_aprobadas
        self.creditos_totales = 0
    
    def getInfo(self):
        return [self.cedula, self.nombre, self.carrera, self.materias, self.uc_aprobadas]
