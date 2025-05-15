
class Nodo:
    def __init__(self, valor=None):
        self.info = valor  # Valor del nodo
        self.prox = None   # Referencia al siguiente nodo


class Cola:
    def __init__(self):
        self.Frente = None  
        self.Final = None  

    def Vacia(self):
        #Verifica si la cola esta vacia
        return self.Frente is None

    def Llena(self):
        #Simula la comprobacion de memoria
        try:
            # crear un nuevo nodo
            nuevo = Nodo()
            return False  # Si se creo correctamente entonces la cola no esta llena
        except MemoryError:
            return True  # Si ocurre un error de memoria se considera que la cola esta llena

    def Insertar(self, valor):
        #Inserta un valor en la cola
        if not self.Llena():
            nuevo = Nodo(valor)  # Crear un nuevo nodo
            nuevo.prox = None     # El siguiente nodo es None al principio
            if self.Final is None:  # Si la cola esta vacia el nuevo nodo se convierte en el frente
                self.Frente = nuevo
            else:  # Si no esta vacia entonces  el nodo final apunta al nuevo nodo
                self.Final.prox = nuevo
            self.Final = nuevo  # El nuevo nodo pasa a ser el nodo Final
            return True
        return False
    def MostrarContenido(self):
        if self.Vacia():
            print("La Cola está vacía.")
        else:
            p = self.Frente
            print("Contenido de la Cola:")
            while p is not None:
                print(p.info)
                p = p.prox
    def Remover(self):
        #Remueve el primer elemento de la cola y lo devuelve
        if not self.Vacia():
            primero = self.Frente  # Tomamos el primer nodo
            valor = primero.info   # Recuperamos el valor de este nodo
            self.Frente = primero.prox  # Avanzamos el Frente al siguiente nodo
            if self.Frente is None:  # Si la cola se vacía después de remover
                self.Final = None
            return valor
        return None  # Si la cola está vacía, no hay nada que remover
