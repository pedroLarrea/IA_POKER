from operator import attrgetter
from carta import Carta

class Jugador:

    # El jugador recibe sus 2 cartas, y el mazo sin sus 2 cartas
    def __init__(self,cartas,mazo):
        self.mano = cartas
        self.restante = mazo
        self.restante.remove(self.mano[0])
        self.restante.remove(self.mano[1])

    # Imprimimos nuestra mano actual
    def verMano(self):
        for m in self.mano:
            m.imprimir()

    # Recibimos la lista de cartas sobre la mesa y calculamos cual es la mejor combinacion de cartas
    def calcularCombinacion(self, mesa, mano):
        
        # unimos las cartas de nuestra mano con los que hay en la mesa en una sola lista
        self.cartas = mano + mesa
        # self.cartas.sort(key = lambda x: x.valor, reverse=True)
        
        # Ordenamos las cartas que tenemos
        self.ordenarMano()

        # Calcular Poker, Full, Color, Trio, Doble Pareja, Pareja, Carta Alta
        # Se almacena nombre_de_la_mano : [arreglo_con_cartas]
        self.manos = {
            'Escalera de Color' : [[]],
            'Poker' : [[]],
            'Full' : [[]],
            'Color' : [[]],
            'Escalera' : [[]],
            'Trio' : [[]],
            'Doble Pareja' : [[]],
            'Par' : [[]],
            'Carta Alta' : [[]]
            }
        
        # Carta Alta
        self.manos['Carta Alta'] = [[self.cartas[0]]]
        
        # Las demas self.manos
        for i in range(0, len(self.cartas) - 1, 1):
            
            par = None
            trio = None
            poker = None
            color = [self.cartas[i]]
            escalera = [self.cartas[i]]
            
            for j in range(i+1, len(self.cartas), 1):

                # Para verificar si existe una escalera
                # Casos a verificar, cuando cuando hay una escalera del tipo 5,4,3,2,A (La A esta al comienzo, no al final)
                # Casos a verificar, Cuando los valores se repiten A, K, K, Q, J, 10, 10 (Una k y un 10 se van a ignorar pudiendose perder escaleras de color)
                if self.cartas[j].valor == ( escalera[-1].valor - 1 ):
                    escalera.append(self.cartas[j])
                if len(escalera) == 5 and self.manos['Escalera'] == [[]]:
                    self.manos['Escalera'] = [escalera]
                
                # Para verificar si existe un color
                if self.cartas[j].palo == self.cartas[i].palo and len(color) < 5:
                    color.append(self.cartas[j])
                if len(color) == 5 and self.manos['Color'] == [[]]:
                    self.manos['Color'] = [color]
                    
                # Para verificar si existe un poker
                if self.cartas[j].valor == self.cartas[i].valor and trio is not None :
                    poker = trio + [self.cartas[j]]
                    if self.manos['Poker'] == [[]]:
                        self.manos['Poker'] = [poker]
                    else:
                        self.manos['Poker'].append(poker)
                
                # Para verificar si existe un trio
                if self.cartas[j].valor == self.cartas[i].valor and par is not None :
                    trio = par + [self.cartas[j]]
                    if self.manos['Trio'] == [[]]:
                        self.manos['Trio'] = [trio]
                    else:
                        self.manos['Trio'].append(trio)
                
                # Para verificar si existe pareja
                if self.cartas[j].valor == self.cartas[i].valor and par is None:
                    par = [self.cartas[i],self.cartas[j]]
                    if self.manos['Par'] == [[]]:
                        self.manos['Par'] = [par]
                    else:
                        self.manos['Par'].append(par)
                
        # Para verificar existencia de doble pareja
        if self.manos['Par'] != [[]]:
            for i in range(0, len(self.manos['Par'])-1, 1):
                for j in range(i+1, len(self.manos['Par']), 1):
                    if self.manos['Par'][i][0].valor != self.manos['Par'][j][0].valor:
                        doblePareja = self.manos['Par'][i] + self.manos['Par'][j]
                        if self.manos['Doble Pareja'] == [[]]:
                            self.manos['Doble Pareja'] = [doblePareja]
                        else:
                            self.manos['Doble Pareja'].append(doblePareja)
        
        # Para verificar existencia de un full
        if self.manos['Par'] != [[]] and self.manos['Trio'] != [[]]:
            for i in range(0, len(self.manos['Par']), 1):
                for j in range(0, len(self.manos['Trio']), 1):
                    if self.manos['Par'][i][0].valor != self.manos['Trio'][j][0].valor:
                        full = self.manos['Par'][i] + self.manos['Trio'][j]
                        if self.manos['Full'] == [[]]:
                            self.manos['Full'] = [full]
                        else:
                            self.manos['Full'].append(full)
        
        # Para verificar existencia de una escalera de color
        if self.manos['Escalera'] != [[]]:
            for escalera in self.manos['Escalera']:
                if escalera[0].palo == escalera[1].palo == escalera[2].palo == escalera[3].palo == escalera[4].palo:
                    if self.manos['Escalera de Color'] == [[]]:
                            self.manos['Escalera de Color'] = [escalera]
                    else:
                            self.manos['Escalera de Color'].append(escalera)
        
        # self.imprimirManosObtenidas()

        # retornar la mejor combinacion
       
        for nombreMano, mano in self.manos.items():
            for i in mano:
                if mano != [[]]:
                    return [nombreMano,mano[0]]
              
    # Calculamos cual es nuestra mejor posibilidad de ganar actualmente
    def calcularProbabilidad(self,mesa):

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

        contadorGanado = 0
        contadorTotal = 0
        
        # Remover las cartas de la mesa del mazo
        for carta in mesa:
            if carta in self.restante:
                self.restante.remove(carta)


        print("Ejecutando calcularProbabilidad...")
        print("len(mesa):",len(mesa))
        print("len(self.restante):",len(self.restante))

        # Calculamos todas las posbiles manos del rival
        for i in range(0, len(self.restante) - 1, 1):
            for j in range(i + 1, len(self.restante), 1):
                
                PCartaRival1 = self.restante[i]
                PCartaRival2 = self.restante[j]

                # Quitar las 2 cartas elegidas para el rival del mazo
                self.restante.remove(PCartaRival1)
                self.restante.remove(PCartaRival2)

                # Condicion cuando conocomos 0 cartas de la mesa
                if mesa == []:
                    for a in range(0,len(self.restante)-4,1):
                        for b in range (a+1,len(self.restante)-3,1):
                            for c in range (b+1,len(self.restante)-2,1):
                                for d in range (c+1,len(self.restante)-1,1):
                                    for e in range (d+1,len(self.restante),1):
                                        # Calculamos la combinacion de cartas del rival
                                        Cconocidas = [self.restante[a],self.restante[b],self.restante[c],self.restante[d],self.restante[e]]
                                        manoRival = self.calcularCombinacion(Cconocidas,[PCartaRival1,PCartaRival2])
                                        manoMia = self.calcularCombinacion(Cconocidas,self.mano)
                                        contadorTotal = contadorTotal + 1
                                        # caso en el que jugador 1 tiene mejor mano que jugador 2
                                        if manosValor[manoMia[0]] > manosValor[manoRival[0]]:
                                            contadorGanado = contadorGanado + 1
                                            
                # Condicion cuando conocomos 3 cartas de la mesa
                if len(mesa) == 3:
                    for a in range(0,len(self.restante)-1,1):
                        for b in range (a+1,len(self.restante),1):
                            # Calculamos la combinacion de cartas del rival
                            Cconocidas = mesa + [self.restante[a],self.restante[b]]
                            manoRival = self.calcularCombinacion(Cconocidas,[PCartaRival1,PCartaRival2])
                            manoMia = self.calcularCombinacion(Cconocidas,self.mano)
                            contadorTotal = contadorTotal + 1
                            # caso en el que jugador 1 tiene mejor mano que jugador 2
                            if manosValor[manoMia[0]] > manosValor[manoRival[0]]:
                                contadorGanado = contadorGanado + 1

                # Condicion cuando conocomos 4 cartas de la mesa
                if len(mesa) == 4:
                    for a in range(0,len(self.restante),1):
                        # Calculamos la combinacion de cartas del rival
                        Cconocidas = mesa + [self.restante[a]]
                        manoRival = self.calcularCombinacion(Cconocidas,[PCartaRival1,PCartaRival2])
                        manoMia = self.calcularCombinacion(Cconocidas,self.mano)
                        contadorTotal = contadorTotal + 1
                        # caso en el que jugador 1 tiene mejor mano que jugador 2
                        if manosValor[manoMia[0]] > manosValor[manoRival[0]]:
                            contadorGanado = contadorGanado + 1

                # Condicion cuando conocomos 5 cartas de la mesa
                if len(mesa) == 5:
                    # Calculamos la combinacion de cartas del rival
                    Cconocidas = mesa
                    manoRival = self.calcularCombinacion(Cconocidas,[PCartaRival1,PCartaRival2])
                    manoMia = self.calcularCombinacion(Cconocidas,self.mano)
                    contadorTotal = contadorTotal + 1
                    # caso en el que jugador 1 tiene mejor mano que jugador 2
                    if manosValor[manoMia[0]] > manosValor[manoRival[0]]:
                        contadorGanado = contadorGanado + 1

                # Poner las 2 cartas elegidas para el rival de nuevo al mazo
                self.restante.insert(i,PCartaRival1)
                self.restante.insert(j,PCartaRival2)

        print("Casos totales :",contadorTotal)
        print("Casos ganadores :",contadorGanado)
        print("Probabilidad de ganar con esta mano (",contadorGanado,"/",contadorTotal,"):",contadorGanado/contadorTotal)

    # Ordenar las cartas para que sea mas facil determinar las manos
    def ordenarMano(self):
        for i in range(0, len(self.cartas) - 1, 1):
            for j in range(i+1, len(self.cartas), 1):
                if self.cartas[j].valor == self.cartas[i].valor:
                    if self.cartas[j].palo > self.cartas[i].palo:
                        aux = self.cartas[i]
                        self.cartas[i] = self.cartas[j]
                        self.cartas[j] = aux
                elif self.cartas[j].valor > self.cartas[i].valor:
                    aux = self.cartas[i]
                    self.cartas[i] = self.cartas[j]
                    self.cartas[j] = aux
  
    def imprimirManosObtenidas(self):
        for nombreMano, mano in self.manos.items():
            print("===",nombreMano,"===")
            for i in mano:
                Carta.imprimirLista(i)
    
    def manoActual(self):
        for nombreMano, mano in self.manos.items():
            if mano != [[]]:
                print(nombreMano,":")
                Carta.imprimirLista(mano[0])
                break
    
    