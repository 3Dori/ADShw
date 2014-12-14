import random

# make sure that SIZE1 + SIZE2 <= CAPACITY
CAPACITY = 100000
#POPULATION = list(map(str, range(-CAPACITY // 100, CAPACITY // 100))) * 2
range_mill = range(-500000, 500000)
population = random.sample(range_mill, 25000) + random.sample(range_mill, 25000) + random.sample(range_mill, 25000) + random.sample(range_mill, 25000)
population = list(map(str, population))

def main():
    small_population = map(str, random.sample(range_mill, 10000))
    with open('test_cases/test_all.txt', 'w') as f:
        f.write(' '.join(small_population))
    #print(' '.join(map(str, POPULATION)))

if __name__ == '__main__':
    main()
