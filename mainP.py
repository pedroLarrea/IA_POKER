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
        [Carta(11, "Corazon"), Carta(12, "Corazon")], mazoOriginal)
    jugador2 = Jugador(
        [mazo.obtenerCarta(), mazo.obtenerCarta()], mazoOriginal)
    jugadores = [jugador1, jugador2]



    jugador1.calcularCombinacion([Carta(10, "Pica"), Carta(10, "Corazon"), Carta(13, "Corazon"), Carta(14, "Diamante"), Carta(14, "Corazon")])
    

