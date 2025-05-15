# comentario

class Nodo:
    def __init__(self, valor=None):
        self.info = valor  # Almacena el valor del nodo
        self.prox = None   # Referencia al siguiente nodo (esto simula el puntero

class Lista:
    def __init__(self):
        self.Primero = None  

    def Vacia(self):
        #Verifica si la lista esta vacia
        return self.Primero is None

    def Llena(self):
        #Simula la comprobacion de memoria
        try:
            nuevo = Nodo() 
            return False  # Si no hay error entonces no esta llena
        except MemoryError:
            return True  # Si ocurre un error de memoria entonces la lista esta llena

    def InsComienzo(self, valor):
        #Inserta un valor al principio de la lista
        if not self.Llena():
            nuevo = Nodo(valor)  
            nuevo.prox = self.Primero  # El puntero 'prox' apunta al primer nodo
            self.Primero = nuevo  # El nuevo nodo pasa a ser el primer nodo
            return True
        return False

    def EliComienzo(self):
        #Elimina el primer nodo de la lista
        if not self.Vacia():
            viejo = self.Primero  # Tomamos el primer nodo
            valor = viejo.info  # Aqui recuperamos su valor
            self.Primero = self.Primero.prox  # El primero apunta al siguiente nodo
            del viejo  # El nodo es eliminado (simulacion de delete)
            return valor
        return None  #Si la listaesta vacia no se puede eliminar

    def InsDespues(self, p, valor):
        #Inserta un valor despues del nodo p
        if not self.Llena() and p is not None:
            nuevo = Nodo(valor)
            nuevo.prox = p.prox  # El nuevo nodo apunta al siguiente de p
            p.prox = nuevo  # El nodo p apunta al nuevo nodo
            return True
        return False

    def EliDespues(self, p):
        #Elimina el nodo despues de p
        if p is None or p.prox is None:
            return None  # Si p es None o p no tiene siguiente entonces no se puede eliminar
        viejo = p.prox  # El siguiente nodo de p
        valor = viejo.info  # Aqui recuperamos el valor del nodo a eliminar
        p.prox = viejo.prox  # El nodo p apunta al siguiente de viejo
        del viejo  # El nodo es eliminado
        return valor

    def ObtProx(self, p):
        #Obtiene el siguiente nodo despues de p"
        return p.prox if p is not None else None

    def AsigProx(self, p, q):
        #Asigna el siguiente nodo de p a q
        if p is not None:
            p.prox = q

    def ObtInfo(self, p):
        #Obtiene la informacion almacenada en el nodo "p"
        return p.info if p is not None else None

    def AsigInfo(self, p, valor):
        #Asigna un valor al nodo p"
        if p is not None:
            p.info = valor

    def Contar(self):
        #Cuenta cuántos elementos tiene la lista
        cont = 0
        p = self.Primero
        while p is not None:
            cont += 1
            p = p.prox
        return cont

    def Buscar(self, valor):
        #Busca un valor en la lista
        p = self.Primero
        while p is not None:
            if p.info == valor:
                return p
            p = p.prox
        return None  # Si no se encuentra el valor devuelve None
    def MostrarContenido(self):
        if self.Vacia():
            print("La Lista está vacía.")
        else:
            p = self.Primero
            print("Contenido de la Lista:")
            while p is not None:
                print(p.info)
                p = p.prox
    def pasarListaAux(self, listaFuente, listaDestino):
        #Pasa todos los elementos de una lista a otra
        valor = None
        while not listaFuente.Vacia():
            valor = listaFuente.EliComienzo()  # Elimina el primer valor de la listaFuente
            listaDestino.InsComienzo(valor)  # Inserta el valor al principio de listaDestino

    def __del__(self):
        #Destructor para liberar los recursos cuando la lista es destruida"""
        while not self.Vacia():
            self.EliComienzo()  # Elimina todos los elementos de la lista
