from operator import attrgetter
from carta import Carta

class Jugador:

    # El jugador recibe sus 2 cartas, y el mazo sin sus 2 cartas
    def __init__(self,cartas,mazo):
        self.mano = cartas
        self.restante = mazo

    # Imprimimos nuestra mano actual
    def verMano(self):
        for m in self.mano:
            m.imprimir()

    # Recibimos la lista de cartas sobre la mesa y calculamos cual es la mejor combinacion de cartas
    def calcularCombinacion(self, mesa):
        
        # unimos las cartas de nuestra mano con los que hay en la mesa en una sola lista
        self.cartas = self.mano + mesa
        # self.cartas.sort(key = lambda x: x.valor, reverse=True)
        
        # Ordenamos las cartas que tenemos
        self.ordenarMano()
        for c in self.cartas:
            c.imprimir()

        # Calcular Poker, Full, Color, Trio, Doble Pareja, Pareja, Carta Alta
        # Se almacena nombre_de_la_mano : [arreglo_con_cartas]
        manos = {
            'Escalera real' : [[]],
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
        manos['Carta Alta'] = [[self.cartas[0]]]
        
        # Las demas manos
        for i in range(0, len(self.cartas) - 1, 1):
            
            par = None
            trio = None
            poker = None
            color = [self.cartas[i]]
            
            for j in range(i+1, len(self.cartas), 1):
                
                # Para verificar si existe un color
                if self.cartas[j].palo == self.cartas[i].palo and len(color) < 5:
                    color.append(self.cartas[j])
                if len(color) == 5 and manos['Color'] == [[]]:
                    manos['Color'] = [color]
                    color = None
                    
                # Para verificar si existe un poker
                if self.cartas[j].valor == self.cartas[i].valor and trio is not None :
                    poker = trio + [self.cartas[j]]
                    if manos['Poker'] == [[]]:
                        manos['Poker'] = [poker]
                    else:
                        manos['Poker'].append(poker)
                
                # Para verificar si existe un trio
                if self.cartas[j].valor == self.cartas[i].valor and par is not None :
                    trio = par + [self.cartas[j]]
                    if manos['Trio'] == [[]]:
                        manos['Trio'] = [trio]
                    else:
                        manos['Trio'].append(trio)
                
                # Para verificar si existe pareja
                if self.cartas[j].valor == self.cartas[i].valor and par is None:
                    par = [self.cartas[i],self.cartas[j]]
                    if manos['Par'] == [[]]:
                        manos['Par'] = [par]
                    else:
                        manos['Par'].append(par)
                
        # Para verificar existencia de doble pareja
        if manos['Par'] != [[]]:
            for i in range(0, len(manos['Par'])-1, 1):
                for j in range(i+1, len(manos['Par']), 1):
                    if manos['Par'][i][0].valor != manos['Par'][j][0].valor:
                        doblePareja = manos['Par'][i] + manos['Par'][j]
                        if manos['Doble Pareja'] == [[]]:
                            manos['Doble Pareja'] = [doblePareja]
                        else:
                            manos['Doble Pareja'].append(doblePareja)
        
        # Para verificar existencia de un full
        if manos['Par'] != [[]] and manos['Trio'] != [[]]:
            for i in range(0, len(manos['Par']), 1):
                for j in range(0, len(manos['Trio']), 1):
                    if manos['Par'][i][0].valor != manos['Trio'][j][0].valor:
                        full = manos['Par'][i] + manos['Trio'][j]
                        if manos['Full'] == [[]]:
                            manos['Full'] = [full]
                        else:
                            manos['Full'].append(full)
        
        self.imprimirManosObtenidas(manos)
        
        


    # Calculamos cual es nuestra mejor posibilidad de ganar actualmente
    def calcularProbabilidad(self):

        # Calculamos todas las posbiles manos del rival
        for i in range(0, len(self.restante) - 1, 1):
            for j in range(i + 1, len(self.restante), 1):
                
                self.restante[i].imprimir()
                self.restante[j].imprimir()

                

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

    
    def imprimirManosObtenidas(self,manos):
        for nombreMano, mano in manos.items():
            print("===",nombreMano,"===")
            for i in mano:
                Carta.imprimirLista(i)
    
    
    