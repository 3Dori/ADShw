import random

# make sure that SIZE1 + SIZE2 <= CAPACITY
CAPACITY = 100000
#POPULATION = list(map(str, range(-CAPACITY // 100, CAPACITY // 100))) * 2
range_mill = range(-500000, 500000)
population = random.sample(range_mill, 25000) + random.sample(range_mill, 25000) + random.sample(range_mill, 25000) + random.sample(range_mill, 25000)
population = list(map(str, population))

def gen_sorted():
    return map(str, range(-50000, 50000, 10))

def gen_reversed():
    return map(str, range(50000, -50000, -10))

def main():
    #small_population = map(str, random.sample(range_mill, 10000))
    data = gen_sorted()
    with open('test_cases/test_sorted.txt', 'w') as f:
        f.write(' '.join(data))
    data = gen_reversed()
    with open('test_cases/test_rev.txt', 'w') as f:
        f.write(' '.join(data))


if __name__ == '__main__':
    main()
