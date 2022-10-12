from operator import attrgetter
from carta import Carta
import pandas as pd


class Jugador:

    # El jugador recibe sus 2 cartas, y el mazo sin sus 2 cartas
    def __init__(self, cartas, mazo):
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
        
        #agregamos las A al final de la mano...
        contador=0
        while self.cartas[contador].valor==14:
            self.cartas.append(Carta(1, self.cartas[contador].palo))
            contador+=1

        # Calcular Poker, Full, Color, Trio, Doble Pareja, Pareja, Carta Alta
        # Se almacena nombre_de_la_mano : [arreglo_con_cartas]
        self.manos = {
            'Escalera de Color': [[]],
            'Poker': [[]],
            'Full': [[]],
            'Color': [[]],
            'Escalera': [[]],
            'Trio': [[]],
            'Doble Pareja': [[]],
            'Par': [[]],
            'Carta Alta': [[]]
        }

        # Carta Alta
        self.manos['Carta Alta'] = [[self.cartas[0]]]

        # para escaleras exclusivo-------------------------------------------------------------------------------------------
        # utilizo numeros binarios, los 2 declarados abajo son el limite inferior y superior desde donde controlar, si es 1 se guarda la posicion y que sean de longitud 5
        
        
        
        binarioString1 = '11111'    #despues se ve cuantos 0 se le agrega
        binarioString2 = ''         #despues se ve cuantos 1 son en total
        
        
        binarioString1 =binarioString1.zfill(len(self.cartas)) #agrega tantos 0's como falten
        for i in range(0, len(self.cartas), 1):
            binarioString2=binarioString2+'1'
            
        
        

        #paso int de la cadena
        binarioInt1 = int(binarioString1, 2)
        binarioInt2 = int(binarioString2, 2)

        

        # ciclo
        while binarioInt1 <= binarioInt2:
            binario1 = bin(binarioInt1)  # binario
            # binario con 0's a la izq y sin 2 valores iniciales que te pone la transformacion
            binario1 = str(binario1[2:]).zfill(len(self.cartas))#aca el binario es tipo 'str'
            
            # print(type(binario1))
            lugar1 = []#guardo posiciones de escalera provisional, la armo dps
            for i in range(0, len(binario1), 1):
                if binario1[i] == '1':
                    # print('entre1')
                    lugar1.append(i)
                    
            binarioInt1 = int(binario1, 2)+1#para la siguiente iteracion

            if len(lugar1) == 5:
                # print('entre2')
                #print(lugar1)
                #print(binario1)
                escaleraAux=[]
                #armo mi posible escalera
                for i in range(0, 5, 1):
                    escaleraAux.append(self.cartas[lugar1[i]])
                
                #impresion de lo que selecciona para la escalera auxiliar
                '''
                print('escalera auxiliar')
                for i in range(0, 5, 1):
                    print(escaleraAux[i].valor, "\t", escaleraAux[i].palo)
                '''
                
                
                #ESCALERA COLOR
                esc=[]#escalera provisional que se va a agregar despues si cumple condiciones
                esc.append(escaleraAux[0])
                for i in range(1, 5, 1):
                    if escaleraAux[i].valor == escaleraAux[i-1].valor-1 and escaleraAux[i].palo == escaleraAux[i-1].palo:       #siempre tendria que entrar aca si es una escalera
                        esc.append(escaleraAux[i])
                    else:#si entra aca, settea vacio y rompe ciclo
                        esc=[]
                        break
                
                if len(esc)==5:    #si es de longitud 5 cumplio y se agrega al conjunto de escaleras colores que se encontraron hasta el momento
                    
                    if self.manos['Escalera de Color'] != [[]]:
                        self.manos['Escalera de Color'].append(esc)
                    else:
                        self.manos['Escalera de Color'] = [esc]
                    continue#esto para que no evalue una escalera normal, ya que va a terminar cumpliendo condiciones
                    
                    
                    #ESCALERA NORMAL
                esc=[]#escalera provisional que se va a agregar despues si cumple condiciones
                esc.append(escaleraAux[0])
                for i in range(1, 5, 1):
                    if escaleraAux[i].valor == escaleraAux[i-1].valor-1:       #siempre tendria que entrar aca si es una escalera
                        esc.append(escaleraAux[i])
                    else:#si entra aca, settea vacio y rompe ciclo
                        esc=[]
                        break
                
                if len(esc)==5:    #si es de longitud 5 cumplio y se agrega al conjunto de escaleras colores que se encontraron hasta el momento
                    if self.manos['Escalera'] != [[]]:
                        self.manos['Escalera'].append(esc)
                    else:
                        self.manos['Escalera'] = [esc]
                                  
        #quito las A's que agregue al final
        contador=0
        while self.cartas[contador].valor==14:
            self.cartas.pop()
            contador+=1
            

       # -----------------------------------------------------------------------------------------------------------------------

       # Las demas self.manos
        for i in range(0, len(self.cartas) - 1, 1):

            par = None
            trio = None
            poker = None
            color = [self.cartas[i]]

            for j in range(i+1, len(self.cartas), 1):

                # Para verificar si existe un color
                if self.cartas[j].palo == self.cartas[i].palo and len(color) < 5:
                    color.append(self.cartas[j])
                if len(color) == 5 and self.manos['Color'] == [[]]:
                    self.manos['Color'] = [color]

                # Para verificar si existe un poker
                if self.cartas[j].valor == self.cartas[i].valor and trio is not None:
                    poker = trio + [self.cartas[j]]
                    if self.manos['Poker'] == [[]]:
                        self.manos['Poker'] = [poker]
                    else:
                        self.manos['Poker'].append(poker)

                # Para verificar si existe un trio
                if self.cartas[j].valor == self.cartas[i].valor and par is not None:
                    trio = par + [self.cartas[j]]
                    if self.manos['Trio'] == [[]]:
                        self.manos['Trio'] = [trio]
                    else:
                        self.manos['Trio'].append(trio)

                # Para verificar si existe pareja
                if self.cartas[j].valor == self.cartas[i].valor and par is None:
                    par = [self.cartas[i], self.cartas[j]]
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
            for i in range(0, len(self.manos['Par'])-1, 1):
                for j in range(0, len(self.manos['Trio'])-1, 1):
                    if self.manos['Par'][i][0].valor != self.manos['Trio'][j][0].valor:
                        full = self.manos['Trio'][j] + self.manos['Par'][i]
                        if self.manos['Full'] == [[]]:
                            self.manos['Full'] = [full]
                        else:
                            self.manos['Full'].append(full)

        # Para verificar existencia de una escalera de color
        '''
        if self.manos['Escalera'] != [[]]:
            for escalera in self.manos['Escalera']:
                if escalera[0].palo == escalera[1].palo == escalera[2].palo == escalera[3].palo == escalera[4].palo:
                    if self.manos['Escalera de Color'] == [[]]:
                        self.manos['Escalera de Color'] = [escalera]
                    else:
                            self.manos['Escalera de Color'].append(escalera)
        '''
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

        if mesa != []:
        
            # Calculamos todas las posbiles manos del rival
            for i in range(0, len(self.restante) - 1, 1):
                for j in range(i + 1, len(self.restante), 1):
                    
                    PCartaRival1 = self.restante[i]
                    PCartaRival2 = self.restante[j]

                    # Quitar las 2 cartas elegidas para el rival del mazo
                    self.restante.remove(PCartaRival1)
                    self.restante.remove(PCartaRival2)
                                                
                    # Condicion cuando conozco 3 cartas de la mesa

                    # No calculamos las posibles 2 cartas sobre la mesa
                    # calculamos las manos posibles con 5 cartas para jugar agresivo en el flop
                    if len(mesa) == 3:
                        # Calculamos la combinacion de cartas del rival
                        Cconocidas = mesa
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

            return (contadorGanado/contadorTotal)*100

        else:
            
            # para los casos en que no conocemos cartas en la mesa, leemos un csv con las probabilidades
            df = pd.read_csv('probabilidadPreFlop.csv',sep=";",names=["1ra. Carta","2da. Carta","palo","probabilidad"])

            # filtrar los datos del dataframe, segun las cartas y si tienen el mismo palo
            mismaMano = "d"
            if self.mano[0].returnPalo() == self.mano[1].returnPalo():
                mismaMano = "m"

            # Ordenamos las cartas que tenemos
            if self.mano[1].returnTrueValor() > self.mano[0].returnTrueValor():
                aux = self.mano[0]
                self.mano[0] = self.mano[1]
                self.mano[1] = aux
            
            dfProbabilidad = df[ (df["1ra. Carta"] == self.mano[0].returnValor()) & (df["2da. Carta"] == self.mano[1].returnValor()) 
            & (df["palo"] == mismaMano) ]
            
            # resultado dfProbabilidad.iloc[0]["probabilidad"]
            self.mano[0].imprimir()
            self.mano[1].imprimir()

            return dfProbabilidad.iloc[0]["probabilidad"]
            
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
            print("===", nombreMano, "===")
            for i in mano:
                Carta.imprimirLista(i)

    def manoActual(self):
        for nombreMano, mano in self.manos.items():
            if mano != [[]]:
                print(nombreMano, ":")
                Carta.imprimirLista(mano[0])
                break

    def retornarMano(self):
        return self.mano