from mesa import Mesa
from mazo import Mazo
from jugador import Jugador
import os
import time

modoJuego = False
os.system ("cls") 
time.sleep(2)
#os.system ("clear") Para linux
print ("--------------------------------------------------------------")
print("==== INTELIGENCIA ARTIFICIAL ====\n")
print("Poker - Texas Hold'em \n")   
print("Opciones:\n")
print("1 - Jugador vs Bot\n")     
print("2 - Bot vs Bot\n") 
print("OTRO - Salir\n")   
print ("--------------------------------------------------------------")
opcion = input()
if(opcion == '1' ):
    modoJuego = True
    juego = Mesa(modoJuego,100.0,8.0,4.0)
elif(opcion == '2'):
    modoJuego = False
    juego = Mesa(modoJuego,100.0,8.0,4.0)
else:
    print("Hasta la proxima!...")
