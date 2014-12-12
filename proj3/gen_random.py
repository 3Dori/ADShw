import random

# make sure that SIZE1 + SIZE2 <= CAPACITY
CAPACITY = 1000000
POPULATION = range(-CAPACITY // 2, CAPACITY // 2)
SIZE1 = 999999
SIZE2 = 1

def main():
    print(CAPACITY)
    print(SIZE1, SIZE2)
    data = random.sample(POPULATION, (SIZE1 + SIZE2))
    #print(len(POPULATION))
    print(' '.join(map(str, data[:SIZE1])))
    print(' '.join(map(str, data[SIZE1:])))

if __name__ == '__main__':
    main()
