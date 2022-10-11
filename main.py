from mesa import Mesa
from mazo import Mazo
from jugador import Jugador

# juego = Mesa(False,100.0,8.0)

# Creamos el mazo para jugar
mazo = Mazo()
mazoOriginal = list(mazo.obtenerMazo())

# Creamos los jugadores y repartimos cartas
jugador1 = Jugador([mazo.obtenerCarta(), mazo.obtenerCarta()], list(mazoOriginal))
mesa = [mazo.obtenerCarta(), mazo.obtenerCarta(), mazo.obtenerCarta()]
jugador1.calcularProbabilidad(mesa)
