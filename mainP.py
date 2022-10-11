from mazo import Mazo
from carta import Carta
from jugador import Jugador
import os
import time


class Mesa:
    # Creamos el mazo para jugar
    mazo = Mazo()
    mazoOriginal = list(mazo.obtenerMazo())

    # Creamos los jugadores y repartimos cartas
    jugador1 = Jugador(
        [Carta(8, "Corazon"), Carta(9, "Corazon")], mazoOriginal)
    jugador2 = Jugador(
        [mazo.obtenerCarta(), mazo.obtenerCarta()], mazoOriginal)
    jugadores = [jugador1, jugador2]



    jugador1.calcularCombinacion([Carta(3, "Pica"), Carta(4, "Corazon"), Carta(5, "Corazon"), Carta(6, "Diamante"), Carta(7, "Corazon")])
    

