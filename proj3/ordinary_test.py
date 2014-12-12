import subprocess
SIZE = 1000000
REPEAT = 10

def get_partition(percentage, max_size):
    return max_size * percentage // 100

def multi_10_from_100(max_size):
    size = 100
    while size <= max_size:
        yield size
        size *= 10

def main():
    methods = {'insert': 0, 'buildheap': 1}
    with open('result.txt', 'w') as f:
        f.write('')    # clear file
    for size in multi_10_from_100(SIZE):
        for percentage in range(0, 110, 10):
            size1 = get_partition(percentage, size // 2)
            size2 = size - size1
            for method in ('insert', 'buildheap'):
                settings = '{} {} {} {}\n'.format(SIZE, size1, size2, methods[method])
                with open('settings.txt', 'w') as setting, open('result.txt', 'a') as result:
                    setting.write(settings)
                    result.write(settings)
                result_sum = 0
                for repeat_count in range(REPEAT):
                    result_sum += float(subprocess.check_output('cat settings.txt test1_input.txt | ./ordinary', shell=True))
                with open('result.txt', 'a') as result:
                    result.write('{:f}'.format(result_sum / REPEAT) + '\n')

if __name__ == '__main__':
    main()
