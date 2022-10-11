
class Carta:

    valores = {
            14 : "A",
            2 : "2",
            3 : "3",
            4 : "4",
            5 : "5",
            6 : "6",
            7 : "7",
            8 : "8",
            9 : "9",
            10 : "10",
            11 : "J",
            12 : "Q",
            13 : "K",
        }
    
    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo

    def imprimir(self):
        print(self.valores[self.valor], "-",self.palo)

    def imprimirLista(listaCartas):
        if listaCartas != []:
            for c in listaCartas:
                c.imprimir()
        else:
            print("Sin cartas")