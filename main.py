from mazo import Mazo
from carta import Carta
from jugador import Jugador

mazo = Mazo()

mazoOriginal = list(mazo.obtenerMazo())

bot = Jugador([mazo.obtenerCarta(), mazo.obtenerCarta()], mazoOriginal)
# bot.verMano()
bot.calcularCombinacion([mazo.obtenerCarta(), mazo.obtenerCarta(), mazo.obtenerCarta()])
# bot.manoActual()
