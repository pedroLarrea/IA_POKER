from mazo import Mazo
from carta import Carta
from jugador import Jugador
import os
import time

class Mesa:

    # Creamos mesa
    # Modo = True -> maquina vs jugador
    
    def __init__(self,modo, cantFichas, ciegaGrande):
        # Creamos el mazo para jugar
        self.mazo = Mazo()
        self.mazoOriginal = list(self.mazo.obtenerMazo())
        
        # Fichas disponible para cada jugador
        # [jugador1, jugador2 o usuario]
        self.fichas = [cantFichas,cantFichas]
        self.apuestas = [0,0]

        # Eestablecemos la ciega grande y pequeña
        self.ciegaGrande = ciegaGrande
        self.ciegaPequeña = ciegaGrande / 2
        
        # Creamos los jugadores y repartimos cartas
        jugador1 = Jugador([self.mazo.obtenerCarta(), self.mazo.obtenerCarta()], self.mazoOriginal)
        jugador2 = Jugador([self.mazo.obtenerCarta(), self.mazo.obtenerCarta()], self.mazoOriginal)
        self.jugadores = [jugador1,jugador2]

        jugador1.calcularCombinacion([])

        # Cartas sobre la mesa
        self.mesa = []
        
        #Empieza el preflop
        self.preflop()

        
    def preflop(self):
        # Bandera para saber cuando termina el flop
        finalizarPreflop = False
        
        # Ciega Grande
        self.apostar(0, self.ciegaGrande)
        
        # Ciega Pequeña
        self.apostar(1, self.ciegaPequeña)

        # Variable para saber el turno de quien es ( 0 = jugador1 , 1 = jugador2 o usuario )
        turno = 1

        # empezar ronda de apuestas
        self.rondaDeApuestas(turno)
    
    # nroJugador ( 0 = jugador1 , 1 = jugador2 o usuario ), cantApuesta = cantidad a apostar
    def apostar(self,nroJugador,cantApuesta):
        # All in
        if cantApuesta >= self.fichas[nroJugador]:
            self.apuestas[nroJugador] = self.fichas[nroJugador]
            self.fichas[nroJugador] = 0
        else:
            self.apuestas[nroJugador] += cantApuesta
            self.fichas[nroJugador] -= cantApuesta

    
    def verMesa(self):
        for i in range(0, len(self.jugadores), 1):
            print("== Jugador",i,"==")
            print("* Cartas :")
            self.jugadores[i].verMano()
            print("* Fichas :",self.fichas[i])
            print("* Apuestas :",self.apuestas[i])

    
    def rondaDeApuestas(self, turno):
        continuar = True
        self.opcionesAcciones(turno)
        

    def opcionesAcciones(self, nroJugador):
        os.system ("cls") 
        time.sleep(1)
        #os.system ("clear") Para linux
        self.verMesa()
        
