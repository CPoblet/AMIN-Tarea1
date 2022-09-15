import sys
import numpy as np

def main(argv):
    print(argv)
    if(len(argv) == 4):
        seed = int(argv[1])
        n = int(argv[2])
        p = int(argv[3])
        print(f'seed {seed}, n {n}, p {p}')

        np.random.seed(seed=seed)
        population = np.zeros((p, n), dtype = int)

        for i in range(p):
            population[i] = np.arange(0, n)
            np.random.shuffle(population[i])
        print(population)


if __name__ == '__main__':
    main(sys.argv)