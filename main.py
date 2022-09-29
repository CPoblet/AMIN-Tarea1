import random
import sys
import numpy as np

'''
    Funcion usada para poder generar una matriz de "n" por "p" 
    donde "n" es el tamaño del tablero y "p" es el tamaño de la poblacion.
'''
def generar_poblacion(n, p):
    poblacion = np.zeros((p, n), dtype=int)
    for i in poblacion:
        i[...] = np.arange(0, n)
        np.random.shuffle(i)
    return poblacion

'''
    Funcion que genera el fitness del individuo pedido.
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
    Funcion para generar una ruleta que esta dividida equivalente al fitness 
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
    Funcion que devuelve la posicion de un individuo a base de la ruleta.
'''
def seleccion_individuo(ruleta):
    rand = random.uniform(0, 1)
    for i in range(len(ruleta)):
        if rand <= ruleta[i]:
            return i

'''
    Funcion que devuelve 2 hijos de la cruza entre 2 individuos distintos dado un punto de corte aleatorio.
'''
def cruzar_individuos(individuo1, individuo2, valor_cruza):
    c = random.randint(0, 100)
    if c <= valor_cruza:
        i_corte = random.randint(0, len(individuo1)-1)
        if i_corte == 0:
            hijo1 = np.concatenate((individuo1[:i_corte+1], individuo2[i_corte+1:]))
            hijo2 = np.concatenate((individuo2[:i_corte+1], individuo1[i_corte+1:]))
        else:
            hijo1 = np.concatenate((individuo1[:i_corte], individuo2[i_corte:]))
            hijo2 = np.concatenate((individuo2[:i_corte], individuo1[i_corte:]))
        return np.array([hijo1, hijo2])
    return np.array([])

'''
    Funcion que es utilizada para arreglar los hijos que generados por la cruza tienen una o mas
    posciciones iguales las cuales se deben cambiadas o modificadas por otra que no se repita. 
'''
def rectificar_hijos(hijos):
    modelo = np.arange(len(hijos[0]))
    valores_faltantes1 = [x for x in modelo if x not in hijos[0]] 
    valores_faltantes2 = [x for x in modelo if x not in hijos[1]]
    indices1 = np.array([], dtype=int)
    indices2 = np.array([], dtype=int)
    for i in range(len(valores_faltantes1)):
        indices1 = np.append(indices1, np.where(hijos[0] == valores_faltantes2[i])[0])
        indices2 = np.append(indices2, np.where(hijos[1] == valores_faltantes1[i])[0])

    hijo1 = hijos[0].tolist()
    hijo2 = hijos[1].tolist()
    indices1 = indices1.tolist()
    indices2 = indices2.tolist()
    while len(valores_faltantes1) > 0 and len(valores_faltantes2) > 0:
        rand_indice1 = random.choice(indices1)
        rand_indice2 = random.choice(indices2)
        rand_valor1 = random.choice(valores_faltantes1)
        rand_valor2 = random.choice(valores_faltantes2)

        hijo1[rand_indice1] = rand_valor1
        hijo2[rand_indice2] = rand_valor2
        valores_faltantes1.remove(rand_valor1)
        valores_faltantes2.remove(rand_valor2)

        index1 = indices1.index(rand_indice1)
        if index1 % 2 != 0 or index1 == len(indices1)-1:
            del indices1[index1-1]
            del indices1[index1-1]
        else:
            del indices1[index1]
            del indices1[index1]
        index2 = indices2.index(rand_indice2)
        if index2 % 2 != 0 or index2 == len(indices2)-1:
            del indices2[index2-1]
            del indices2[index2-1]
        else:
            del indices2[index2]
            del indices2[index2]
    return np.array([hijo1, hijo2])

'''
    Funcion que intercambia 2 posiciones de un individuo.
'''
def mutacion(individuo):
    indice1 = random.randint(0, len(individuo)-1)
    indice2 = random.randint(0, len(individuo)-1)
    while indice1 == indice2:
        indice1 = random.randint(0, len(individuo)-1)
        indice2 = random.randint(0, len(individuo)-1)
    individuo[indice1], individuo[indice2] = individuo[indice2], individuo[indice1]
    return individuo

def main(argv):
    if (len(argv) == 7):
        seed = int(argv[1]) # Semilla  
        n = int(argv[2])    # Tamaño del tablero
        p = int(argv[3])    # Tamaño de la poblacion
        cruza = int(argv[4])# Porcentaje de cruza 
        muta = int(argv[5]) # Porcentaje de mutacion
        max_i = int(argv[6])# Maximo de iteraciones o generaciones
        print(f'seed {seed}, n {n}, p {p}')
        np.random.seed(seed=seed)

        poblacion = generar_poblacion(n, p)
        for j in range(max_i):# aca inicia 
            print(j)
            fitness_values = np.array([], dtype=int)
            for i in poblacion:
                value = fitness(i, n)
                if value == (n*n)-n: # En caso de tener un fitness perfecto termina la ejecución.
                    print('encontrado')
                    print(i)
                    sys.exit()
                fitness_values = np.append(fitness_values, value)

            ruleta_values = generar_ruleta(fitness_values)

            poblacion_hijos = np.zeros((p, n), dtype=int)
            index = 0
            while index < p:
                encontrados = False
                individuo1 = seleccion_individuo(ruleta_values)
                while not encontrados:
                    individuo2 = seleccion_individuo(ruleta_values)
                    if individuo1 != individuo2:
                        encontrados = True
                individuo1 = poblacion[individuo1]
                individuo2 = poblacion[individuo2]

                hijos = cruzar_individuos(individuo1, individuo2, cruza)
                if len(hijos) != 0:
                    if len(np.unique(hijos[0])) != len(hijos[0]):
                        hijos = rectificar_hijos(hijos)
                    rand_mutacion = random.randint(0, 100)
                    if rand_mutacion <= muta:
                        hijos[0] = mutacion(hijos[0])
                        hijos[1] = mutacion(hijos[1])
                    for i in hijos:
                        if index < p:
                            poblacion_hijos[index] = i
                            index += 1

            poblacion = poblacion_hijos
            print(poblacion)
    else:
        print('Error: Parametros incorrectos')


if __name__ == '__main__':
    main(sys.argv)
