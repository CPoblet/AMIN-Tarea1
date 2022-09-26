import random
import sys
import numpy as np


def generar_poblacion(n=8, p=10):
    poblacion = np.zeros((p, n), dtype=int)
    for i in poblacion:
        i[...] = np.arange(0, n)
        np.random.shuffle(i)
    return poblacion


def fitness(individuo, n):
    count = 0
    max_choques = (n*n)-n
    for i in range(len(individuo)):
        for j in range(len(individuo)):
            if (abs(i-j) == abs(individuo[i]-individuo[j]) and i != j):
                count += 1
    return max_choques - count


def ruleta(fitness):
    suma = np.sum(fitness)
    ruleta = np.array([])
    proporcion = fitness[0]/suma
    ruleta = np.append(ruleta, proporcion)
    for i in range(1, len(fitness)):
        proporcion = fitness[i]/suma
        ruleta = np.append(ruleta, ruleta[i-1]+proporcion)
    return ruleta


def seleccion_individuo(ruleta):
    for i in range(len(ruleta)):
        rand = random.uniform(0, 1)
        if rand <= ruleta[i]:
            return i


def main(argv):
    if (len(argv) == 6):
        seed = int(argv[1])
        n = int(argv[2])
        p = int(argv[3])
        cruza = int(argv[4])
        max_i = int(argv[5])
        print(f'seed {seed}, n {n}, p {p}')
        np.random.seed(seed=seed)

        poblacion = generar_poblacion(n, p)
        print(poblacion)

        fitness_values = np.array([], dtype=int)
        for i in poblacion:
            fitness_values = np.append(fitness_values, fitness(i, n))
        print(fitness_values)

        ruleta_values = ruleta(fitness_values)
        print(ruleta_values)

        encontrados = False
        individuo = seleccion_individuo(ruleta_values)
        while not encontrados:
            individuo2 = seleccion_individuo(ruleta_values)
            if individuo != individuo2:
                encontrados = True
        print(individuo)
        print(individuo2)

        c = random.randint(0, 100)
        print(c)
        if c <= cruza:
            print(poblacion[individuo])
            print(poblacion[individuo2])
        #print(random.uniform(0, 1))
        #solucion = np.array([0, 4, 7, 5, 2, 6, 1, 3])
        #max_choques = np.array([0, 1, 2, 3, 4, 5, 6, 7])
        #print(f'prueba: {fitness(solucion, n)}')
    else:
        print('Error: Parametros incorrectos')


if __name__ == '__main__':
    main(sys.argv)
