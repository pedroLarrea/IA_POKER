from sqlite3 import Time
import time
import random
from carta import Carta

class Mazo:

    # Creamos el mazo obteniendo una combinacion aleatoria del diccionario cartas
    def __init__(self):
        
        self.mazo = []
        cartas = {
            14 : ["Trébol", "Corazon", "Pica", "Diamante"],
            2 : ["Trébol", "Corazon", "Pica", "Diamante"],
            3 : ["Trébol", "Corazon", "Pica", "Diamante"],
            4 : ["Trébol", "Corazon", "Pica", "Diamante"],
            5 : ["Trébol", "Corazon", "Pica", "Diamante"],
            6 : ["Trébol", "Corazon", "Pica", "Diamante"],
            7 : ["Trébol", "Corazon", "Pica", "Diamante"],
            8 : ["Trébol", "Corazon", "Pica", "Diamante"],
            9 : ["Trébol", "Corazon", "Pica", "Diamante"],
            10 : ["Trébol", "Corazon", "Pica", "Diamante"],
            11 : ["Trébol", "Corazon", "Pica", "Diamante"],
            12 : ["Trébol", "Corazon", "Pica", "Diamante"],
            13 : ["Trébol", "Corazon", "Pica", "Diamante"],
        }

        while len(cartas.items()) != 0:

            # random.seed(time.time())

            # elijimos un elemento del diccionario aleatoriamente
            valor, listaPalos = random.choice(list(cartas.items()))
            palo = random.choice(listaPalos)
            
            # agregamos la carta al mazo
            self.mazo.append(Carta(valor,palo))
            
            # Removemos el palo para ese valor
            cartas[valor].remove(palo)
            
            #Si un valor ya no tiene palos disponible, quitamos ese valor de la lista
            if cartas[valor] == []:
                cartas.pop(valor)


    def printMazo(self):
        for c in self.mazo:
            c.imprimir()
        print("Cantidad de cartas en el mazo:",len(self.mazo))


    def obtenerMazo(self):
        return self.mazo
        

    def obtenerCarta(self):
        carta = self.mazo[0]
        self.mazo.remove(carta)
        return carta
