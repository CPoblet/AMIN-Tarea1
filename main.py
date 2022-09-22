import sys
import numpy as np


def generar_poblacion(n=8, p=10):
    poblacion = np.zeros((p, n), dtype=int)

    for i in poblacion:
        i[...] = np.arange(0, n)
        np.random.shuffle(i)
    return poblacion


def fitness(individuo):
    count = 0
    for i in range(len(individuo)):
        for j in range(len(individuo)):
            if (abs(i-j) == abs(individuo[i]-individuo[j]) and i != j):
                count += 1
    return count


def main(argv):
    if (len(argv) == 4):
        seed = int(argv[1])
        n = int(argv[2])
        p = int(argv[3])
        print(f'seed {seed}, n {n}, p {p}')

        np.random.seed(seed=seed)
        poblacion = generar_poblacion(n, p)
        print(poblacion)
        for i in poblacion:
            print(fitness(i))
    else:
        print('Error: Parametros incorrectos')


if __name__ == '__main__':
    main(sys.argv)
