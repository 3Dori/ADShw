#!/usr/local/bin/python3

import subprocess
SIZE = 1000000
REPEAT = 1

def get_partition(percentage, max_size):
    return max_size * percentage // 100

def multi_10_from_100(max_size):
    size = 100
    while size <= max_size:
        yield size
        size *= 10

def ordinary_test():
    size_set = (1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 100000, 200000, 400000, 600000, 800000, 1000000)
    #size_set = (1000, 10000, 100000, 1000000)
    methods = {'insert': 0, 'buildheap': 1}
    with open('ordinary_result.txt', 'w') as f:
        f.write('')    # clear file
    #for size in multi_10_from_100(SIZE):
    for size in size_set:
        for percentage in range(0, 110, 10):
            size1 = get_partition(percentage, size // 2)
            size2 = size - size1
            for method in ('insert', 'buildheap'):
                settings = '{} {} {} {}\n'.format(SIZE, size1, size2, methods[method])
                with open('settings.txt', 'w') as setting, open('ordinary_result.txt', 'a') as result:
                    setting.write(settings)
                    result.write(settings)
                result_sum = 0
                for repeat_count in range(REPEAT):
                    result_sum += float(subprocess.check_output('cat settings.txt test1_input.txt | ./ordinary', shell=True))
                with open('ordinary_result.txt', 'a') as result:
                    result.write('{:f}\n'.format(result_sum / REPEAT))

def ordinary_leftist_skew():
    size_set = range(0, 10001, 50)
    merges = 100
    program = 'ordinary'

    with open('ordinary_result.txt', 'w') as f:
        f.write('')
    for size in size_set:
        settings = '{} {}\n'.format(size, merges)
        with open('settings.txt', 'w') as f:
            f.write(settings)
        with open('ordinary_result.txt', 'a') as f:
            f.write('{} {}'.format(program, settings))
            time = 0
            for rpt in range(REPEAT):
                time += float(subprocess.check_output('./{}'.format(program), shell=True))
            time /= REPEAT
            f.write('{:f}\n'.format(time))


def leftist_test_correctness():
    files = ('skew_recur', 'skew_iter', 'skew_btmup', 'leftist')
    tests = ('test1_input.txt', 'test2_input.txt')
    for a_file in files:
        for test in tests:
            subprocess.call('cat settings.txt {} | ./{} > out.txt'.format(test, a_file), shell=True)
            with open('out.txt', 'r') as f:
                seq = list(map(int, f.read().split()))
            print(seq == sorted(seq))


def leftist_skew_time():
    size_set = range(0, 10001, 50)
    merges_set = (100,)
    programs = ('leftist', 'skew_recur', 'skew_iter', 'skew_btmup')
    with open('leftist_skew_result.txt', 'w') as f:
        f.write('')

    for size in size_set:
        for merges in merges_set:
            settings = "{} {}\n".format(size, merges)
            with open('settings.txt', 'w') as f:
                f.write(settings)
            with open('leftist_skew_result.txt', 'a') as f:
                for program in programs:
                    f.write('{} {}'.format(program, settings))
                    time = 0
                    for rpt in range(REPEAT):
                        time += float(subprocess.check_output('./{}'.format(program), shell=True))
                    time /= REPEAT
                    f.write('{:f}\n'.format(time))


if __name__ == '__main__':
    #leftist_test_correctness()
    #leftist_skew_time()
    ordinary_leftist_skew()
    #ordinary_test()
