import random
import sys
import numpy as np

def random_entero(n):
    return np.random.randint(0, n-1)

'''
    Función usada para poder generar una matriz de "n" por "p" 
    donde "n" es el tamaño del tablero y "p" es el tamaño de la población.
'''
def generar_colonia(n):
    poblacion = np.zeros((n, n), dtype=int)
    for i in range(len(poblacion)):
        poblacion[i][0] = random_entero(n) 
        
    return poblacion

'''
    Función que genera el fitness del individuo pedido.
'''
def fitness(individuo, n):
    count = 0
    max_choques = (n*n)-n
    for i in range(len(individuo)):
        for j in range(len(individuo)):
            if (abs(i-j) == abs(individuo[i]-individuo[j]) and i != j):
                count += 1
    return max_choques - count

'''
    Función para generar una ruleta que esta dividida equivalente al fitness 
    de cada individuo.
'''
def generar_ruleta(fitness):
    suma = np.sum(fitness)
    ruleta = np.array([])
    proporcion = fitness[0]/suma
    ruleta = np.append(ruleta, proporcion)
    for i in range(1, len(fitness)):
        proporcion = fitness[i]/suma
        ruleta = np.append(ruleta, ruleta[i-1]+proporcion)
    return ruleta

'''
    Función que devuelve la posición de un individuo a base de la ruleta.
'''
def seleccion_individuo(ruleta):
    rand = random.uniform(0, 1)
    for i in range(len(ruleta)):
        if rand <= ruleta[i]:
            return i

def main(argv):
    if (len(argv) == 2):
        colonia = int(argv[1])
        """     
        archivo_entrada = argv[1]
        semilla = argv[2]
        colonia = argv[3]
        iteraciones = argv[4]
        evaporacion = argv[5]
        heuristica = argv[6]
        prob_limite = argv[7] 
        """

        print(generar_colonia(colonia))

    else:
        print('Error: Parámetros incorrectos')


if __name__ == '__main__':
    main(sys.argv)

