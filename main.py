from mazo import Mazo
from carta import Carta
from jugador import Jugador

maso = Mazo()

bot = Jugador([maso.obtenerCarta(), maso.obtenerCarta()], maso.obtenerMazo())
bot.calcularCombinacion([maso.obtenerCarta(), 
                        maso.obtenerCarta(),
                        maso.obtenerCarta(),
                        maso.obtenerCarta(),
                        maso.obtenerCarta()])