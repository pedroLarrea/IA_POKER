from mazo import Mazo
from carta import Carta
from jugador import Jugador
import os
import time

class Mesa:

    # Creamos mesa
    # Modo = True -> maquina vs jugador    
    def __init__(self,modo, cantFichas, ciegaGrande):
        
        # Fichas disponible para cada jugador
        # [jugador1, jugador2 o usuario]
        self.fichas = [cantFichas,cantFichas]
        self.apuestas = [0,0]

        # Eestablecemos la ciega grande y pequeña
        self.ciegaGrande = ciegaGrande
        self.ciegaPequeña = ciegaGrande / 2

        self.jugar()

    # jugar siempre que ambos jugadores puedan seguir apostando
    def jugar(self):

        while self.fichas[0] > 0 and self.fichas[1] > 0:
            # Creamos el mazo para jugar
            self.mazo = Mazo()
            self.mazoOriginal = list(self.mazo.obtenerMazo())

            # Creamos los jugadores y repartimos cartas
            jugador1 = Jugador([self.mazo.obtenerCarta(), self.mazo.obtenerCarta()], list(self.mazoOriginal))
            jugador2 = Jugador([self.mazo.obtenerCarta(), self.mazo.obtenerCarta()], list(self.mazoOriginal))
            self.jugadores = [jugador1,jugador2]
            
            # Cartas sobre la mesa
            self.mesa = []
            
            #Empieza el preflop
            self.preflop()

            #Empieza el flop
            self.flop()
            
            #Empieza el turn
            self.turn()
            
            #Empieza el river
            self.river()

            # verificar quien gano la ronda
            self.verificarGanador()        

    # momento del juego cuando aun no hay ninguna carta sobre la mesa        
    def preflop(self):
        # Ciega Grande
        self.apostar(0, self.ciegaGrande)
        
        # Ciega Pequeña
        self.apostar(1, self.ciegaPequeña)

        # Variable para saber el turno de quien es ( 0 = jugador1 , 1 = jugador2 o usuario )
        turno = 1

        # empezar ronda de apuestas
        self.rondaDeApuestas(turno)

        print("Fin del preflop")
    
    # momento del juego cuando ya hay 3 cartas sobre la mesa        
    def flop(self):
        if self.apuestas[0] > 0 and self.apuestas[1] > 0:
            # Cartas sobre la mesa
            self.mesa = [self.mazo.obtenerCarta(),self.mazo.obtenerCarta(),self.mazo.obtenerCarta()]
            
            # Variable para saber el turno de quien es ( 0 = jugador1 , 1 = jugador2 o usuario )
            turno = 1

            # empezar ronda de apuestas
            self.rondaDeApuestas(turno)

            print("Fin del flop")
    
    # momento del juego cuando ya hay 4 cartas sobre la mesa        
    def turn(self):
        if self.apuestas[0] > 0 and self.apuestas[1] > 0:
            # Cartas sobre la mesa
            self.mesa.append(self.mazo.obtenerCarta())
            
            # Variable para saber el turno de quien es ( 0 = jugador1 , 1 = jugador2 o usuario )
            turno = 1

            # empezar ronda de apuestas
            self.rondaDeApuestas(turno)

            print("Fin del turn")
    
    # momento del juego cuando ya hay 5 cartas sobre la mesa        
    def river(self):
        if self.apuestas[0] > 0 and self.apuestas[1] > 0:
            # Cartas sobre la mesa
            self.mesa.append(self.mazo.obtenerCarta())
            
            # Variable para saber el turno de quien es ( 0 = jugador1 , 1 = jugador2 o usuario )
            turno = 1

            # empezar ronda de apuestas
            self.rondaDeApuestas(turno)

            print("Fin del river")

    # nroJugador ( 0 = jugador1 , 1 = jugador2 o usuario ), cantApuesta = cantidad a apostar
    def apostar(self,nroJugador,cantApuesta):
        # All in
        if cantApuesta > 0:
            if cantApuesta >= self.fichas[nroJugador]:
                self.apuestas[nroJugador] = self.fichas[nroJugador]
                self.fichas[nroJugador] = 0
            else:
                self.apuestas[nroJugador] += cantApuesta
                self.fichas[nroJugador] -= cantApuesta
   
    # Ver la mesa actual, mano de los jugadores y apuestas de los mismos
    def verMesa(self):
        for i in range(0, len(self.jugadores), 1):
            print("== Jugador",i+1,"==")
            print("* Cartas :")
            self.jugadores[i].verMano()
            print("* Fichas :",self.fichas[i])
            print("* Apuestas :",self.apuestas[i])
        print("Cartas sobre la mesa:")
        Carta.imprimirLista(self.mesa)
    
    #Ver mano del jugador
    def verManoJugador(self,jugador):
        print("=== Jugador",jugador+1,"===")
        print("* Cartas :")
        self.jugadores[jugador].verMano()
        print("* Fichas :",self.fichas[jugador])
        print("* Tu Apuesta :",self.apuestas[jugador])
        if jugador == 0:
            jugador = 1
        else:
            jugador = 0
        print("* Apuesta del rival :",self.apuestas[jugador])
        print("* Cartas sobre la mesa:")
        Carta.imprimirLista(self.mesa)

    # Por ahora la maquina siempre pasa(check) o iguala la apuesta(call)
    # mostrar opciones para el jugador siempre que tenga fichas
    def rondaDeApuestas(self, turno):
        continuar = True
        jugadasJ1 = jugadasJ2 = False
        
        # self.apuestas[0] > 0 and self.apuestas[1] > 0 -> si alguien no tiene apuestas significa que se retiro de la mesa
        # self.fichas[0] == 0 or self.fichas[1] == 0 -> significa que alguien esta en all-in
        while(continuar and self.apuestas[0] > 0 and self.apuestas[1] > 0):

            # Si turno = 1 juega el usuario, si turno = 0 juega la maquina
            if turno == 1:
                if self.apuestas[1] <= self.apuestas[0] and self.fichas[1] > 0:
                    self.opcionesAcciones(turno)
                jugadasJ2 = True
            else:
                if self.apuestas[0] <= self.apuestas[1] and self.fichas[0] > 0:
                    # Si no coincide la apuesta hacer call
                    if self.apuestas[turno] !=  self.apuestas[1]:
                        self.hacerCall(turno)
                jugadasJ1 = True
                
            # Si ambos jugadores han jugado almenos una ronda y tienen la misma apuesta termina la ronda de apuestas
            # validar cuando no son apuestas iguales
            if jugadasJ1 == jugadasJ2 and ( (self.apuestas[0] == self.apuestas[1]) or self.fichas[0] == 0 or self.fichas[1] == 0):
                continuar = False

            # Para cambiar el turno
            if turno == 0:
                turno = 1
            else:
                turno = 0                                   

    # Para que el jugador haga un call
    def hacerCall(self,nroJugador):
        if nroJugador == 0:
            nroContrincante = 1
        else:
            nroContrincante = 0
        apuesta = self.apuestas[nroContrincante] - self.apuestas[nroJugador]
        self.apostar(nroJugador,  apuesta)
    
    # Para que el jugador haga un raise
    # Puede apostar como minimo lo que falta para alcanzar al otro jugador y como maximo las fichas que tiene
    # elegir el menor entre la diferencia y sus fichas (condicion)
    def hacerRaise(self, nroJugador):
        print("Apostar : ")
        apuesta = int(input())
        while apuesta > self.fichas[nroJugador] or apuesta <= 0:
            print("No se puede apostar esa cantidad")
            apuesta = int(input())
        self.apostar(nroJugador, apuesta)

    # Para que el jugador haga un fold
    def hacerFold(self, nroJugador):
        contrincante = 0
        if nroJugador == 0:
            contrincante = 1
        totalApuesta = self.apuestas[0] + self.apuestas[1]
        self.fichas[contrincante] += totalApuesta
        self.apuestas[0] = self.apuestas[1] = 0

        print("Jugador ",nroJugador+1,"se ha retirado")

    # Opciones para el usuario durante la partida
    def opcionesAcciones(self, nroJugador):
        continuar = True
        while continuar:
            if self.apuestas[0] == self.apuestas[1]:
                continuar = self.opcionesAccionesCheck(nroJugador)
            else:
                continuar = self.opcionesAccionesCall(nroJugador)
            
    # Opciones para el usuario durante la partida cuando las apuestas estan igualadas
    def opcionesAccionesCheck(self,nroJugador):
        continuar = True
        os.system ("cls") 
        time.sleep(2)
        #os.system ("clear") Para linux
        self.verManoJugador(1)
        print("==== Acciones ====")
        print("1 - Check (Pasar)")
        print("2 - Raise (Aumentar)")
        print("3 - Fold (Retirase)")
        opcion = input()

        if(opcion == '1' ): # Check
            continuar = False
        elif(opcion == '2'): # Raise
            continuar = False
            self.hacerRaise(nroJugador)
        elif(opcion == '3'):# Fold
            self.hacerFold(nroJugador)
            continuar = False
        return continuar
    
    # Opciones para el usuario durante la partida cuando las apuestas no estan igualadas
    def opcionesAccionesCall(self,nroJugador):
        continuar = True
        os.system ("cls") 
        time.sleep(2)
        #os.system ("clear") Para linux
        self.verManoJugador(1)
        print("==== Acciones ====")
        print("1 - Call (Igualar)")
        print("2 - Raise (Aumentar)")
        print("3 - Fold (Retirase)")
        opcion = input()

        if(opcion == '1'): # Call
            continuar = False
            self.hacerCall(nroJugador)
        elif(opcion == '2'): # Raise
            continuar = False
            self.hacerRaise(nroJugador)
        elif(opcion == '3'):# Fold
            self.hacerFold(nroJugador)
            continuar = False
        return continuar

    # Verificar quien gano la ronda
    def verificarGanador(self):
        if self.apuestas[0] > 0 and self.apuestas[1] > 0:
            print("Mejor mano de jugador 1")
            manoFinalJ1 = self.jugadores[0].calcularCombinacion(self.mesa,self.jugadores[0].retornarMano())
            print(manoFinalJ1[0])
            Carta.imprimirLista(manoFinalJ1[1])

            print("Mejor mano de jugador 2 o usuario")
            manoFinalJ2 = self.jugadores[1].calcularCombinacion(self.mesa,self.jugadores[1].retornarMano())
            print(manoFinalJ2[0])
            Carta.imprimirLista(manoFinalJ2[1])

            totalApuesta = self.apuestas[0] + self.apuestas[1]

            manosValor = {
                'Escalera de Color' : 9,
                'Poker' : 8,
                'Full' : 7,
                'Color' : 6,
                'Escalera' : 5,
                'Trio' : 4,
                'Doble Pareja' : 3,
                'Par' : 2,
                'Carta Alta' : 1
                }

            # caso en el que jugador 1 tiene mejor mano que jugador 2
            if manosValor[manoFinalJ1[0]] > manosValor[manoFinalJ2[0]]:
                self.fichas[0] += totalApuesta
                print("Jugador 1 gana",totalApuesta,"fichas")
            # caso en el que jugador 2 tiene mejor mano que jugador 1
            elif manosValor[manoFinalJ2[0]] > manosValor[manoFinalJ1[0]]:
                self.fichas[1] += totalApuesta
                print("Jugador 2 gana",totalApuesta,"fichas")
            # empate de manos, verificar cual tiene mayor valor.
            else:
                print("Empate")
                self.fichas[0] += self.apuestas[0]
                self.fichas[1] += self.apuestas[1]
                print("Jugador 1 gana",self.apuestas[0],"fichas")
                print("Jugador 2 gana",self.apuestas[1],"fichas")

            self.apuestas[0] = self.apuestas[1] = 0

        print("Presione enter para continua...")
        input()
        
