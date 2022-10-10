# Calcular los subconjuntos de 3, 4 y 5 

numeros = [10,3,5,9,7,8,1,6,2,4]

# Calcular subconjuntos de 3
contador = 0
for x in range(0,len(numeros)-2,1):
    for y in range (x+1,len(numeros)-1,1):
        for z in range (y+1,len(numeros),1):
            print(numeros[x],numeros[y],numeros[z])
            contador = contador + 1

print(contador)
