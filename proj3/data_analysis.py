#!/usr/bin/python

import collections
import matplotlib.pyplot as plt
from xlwt import *

Data = collections.namedtuple('Data', ['size', 'ratio', 'method', 'time'])    # define Data tuple

def read_data_ordinary():
    SETTING, RESULT = 0, 1
    methods = {'0': 'insert', '1': 'buildheap'}

    data = []
    with open('ordinary_result.txt', 'r') as f:
        raw_data = f.readlines()
    line_state = SETTING
    for line in raw_data:
        if line_state == SETTING:    # format: "capacity size1 size2 method"
            tmp_data = line.split()
            tmp_size = int(tmp_data[1]) + int(tmp_data[2])
            tmp_ratio = float(tmp_data[1]) / float(tmp_data[2])
            tmp_method = methods[tmp_data[3]]
            line_state = RESULT
        elif line_state == RESULT:    # format: "time"
            tmp_time = float(line)
            data.append(Data(tmp_size, tmp_ratio, tmp_method, tmp_time))
            line_state = SETTING
    return data


def read_data_leftist_skew(path='leftist_skew_result.txt'):
    SETTING, RESULT = 0, 1

    data = []
    with open(path, 'r') as f:
        raw_data = f.readlines()
    line_state = SETTING
    for line in raw_data:
        if line_state == SETTING:    # format: "method size merges"
            tmp_data = line.split()
            tmp_method = tmp_data[0]
            tmp_size = int(tmp_data[1])
            tmp_ratio = int(tmp_data[2])
            line_state = RESULT
        elif line_state == RESULT:
            tmp_time = float(line)
            data.append(Data(tmp_size, tmp_ratio, tmp_method, tmp_time))
            line_state = SETTING
    return data


def write_data(data):
    #insert_data, buildheap_data = separate_by_method(data)

    wb = Workbook()
    ws = wb.add_sheet('ordinary_heap')
    ws.write(0, 0, 'size')
    ws.write(0, 1, 'ratio')
    ws.write(0, 2, 'method')
    ws.write(0, 3, 'time')

    row = 1
    for record in data:
        ws.write(row, 0, record.size)
        ws.write(row, 1, record.ratio)
        ws.write(row, 2, record.method)
        ws.write(row, 3, record.time)
        row += 1

    wb.save('test_report.xls')


def plot_time_ratio_ordinary(data):
    size_set = (1000, 10000, 100000, 1000000)
    method_set = ('insert', 'buildheap')
    style_set = ('r--', 'r:', 'b--', 'b:', 'g--', 'g:', 'c--', 'c:', 'm--', 'm:')
    plot_data = [[0], 'k--', [0], 'k:']    # initialize lines as black for a general legend

    # data -> curves
    style_index = 0
    for size in size_set:
        for method in method_set:
            ratio_time_tuple = [(record.ratio, record.time)
                                for record in data
                                if record.size == size and record.method == method]    # [(ratio1, time1), (ratio2, time2), ...]
            ratio_time = zip(*ratio_time_tuple)    # [(ratio1, ratio2, ...), (time1, time2, ...)]
            style = style_set[style_index]
            plot_data += [ratio_time[0], ratio_time[1], style]
            style_index += 1

    plt.plot(*plot_data)
    plt.semilogy()
    plt.xlabel(r'$\frac{\mathrm{\mathsf{heap1.size}}}{\mathrm{\mathsf{heap2.size}}}$', fontsize=20)
    plt.ylabel('time (s)')
    plt.title('time - ratio relationship of merging operation on ordinary heaps')

    plt.text(0.6, 0.02, r'$\mathrm{\mathsf{size=10^6}}$')
    plt.text(0.6, 0.002, r'$\mathrm{\mathsf{size=10^5}}$')
    plt.text(0.6, 0.0003, r'$\mathrm{\mathsf{size=10^4}}$')
    plt.text(0.6, 0.00004, r'$\mathrm{\mathsf{size=1,000}}$')

    plt.legend(['insert', 'buildheap'], loc='upper left')
    plt.savefig('time_ratio_ordinary.pdf', format='pdf', bbox_inches='tight', pad_inches=0.2)
    plt.savefig('time_ratio_ordinary', bbox_inches='tight', pad_inches=0.2)
    plt.clf()
    #plt.show()


def plot_time_size_ordinary(data):
    insert_tuple_data = [(record.size, record.time)
                         for record in data
                         if record.method == 'insert' and record.ratio == 1]
    buildheap_tuple_data = [(record.size, record.time)
                            for record in data
                            if record.method == 'buildheap' and record.ratio == 1]
    insert_data = zip(*insert_tuple_data)
    buildheap_data = zip(*buildheap_tuple_data)
    plot_data = [insert_data[0], insert_data[1], 'r--',
                 buildheap_data[0], buildheap_data[1], 'r:']

    plt.plot(*plot_data)
    #plt.loglog()
    plt.xlabel('size')
    plt.ylabel('time (s)')
    plt.title('time - size relationship of merging operation on ordinary heaps')
    plt.text(800000, 0.018, 'insert')
    plt.text(800000, 0.007, 'buildheap')
    plt.text(200000, 0.015, 'heap1.size = heap2.size')
    plt.savefig('time_size_ordinary.pdf', format='pdf')
    plt.savefig('time_size_ordinary')
    plt.clf()
    #plt.show()


def plot_time_merges_leftist_skew(data):
    size_set = (100000,)
    #merges_set = (2, 3, 4, 5, 10, 20, 40, 100)
    style_set = ('r-', 'b-', 'g-', 'y-', 'm-', 'r:', 'b:', 'g:', 'y:', 'm:')

    plot_data = []
    style_offset = 0
    for size in size_set:
        leftist_iter = [(record.ratio, record.time / record.ratio)
                        for record in data
                        if record.method == 'leftist_iter' and record.size == size]
        leftist_recur = [(record.ratio, record.time / record.ratio)
                         for record in data
                         if record.method == 'leftist_recur' and record.size == size]
        skew_recur = [(record.ratio, record.time / record.ratio)
                      for record in data
                      if record.method == 'skew_recur' and record.size == size]
        skew_iter = [(record.ratio, record.time / record.ratio)
                     for record in data
                     if record.method == 'skew_iter' and record.size == size]
        skew_btmup = [(record.ratio, record.time / record.ratio)
                      for record in data
                      if record.method == 'skew_btmup' and record.size == size]
        leftist_recur, leftist_iter, skew_recur, skew_iter, skew_btmup = zip(*leftist_recur), zip(*leftist_iter), zip(*skew_recur), zip(*skew_iter), zip(*skew_btmup)    # format: "[(merges1, merges2, ...), (time1, time2, ...)]"
        plot_data += [leftist_recur[0], leftist_recur[1], style_set[0 + style_offset],
                      leftist_iter[0], leftist_iter[1], style_set[1 + style_offset],
                      skew_recur[0], skew_recur[1], style_set[2 + style_offset],
                      skew_iter[0], skew_iter[1], style_set[3 + style_offset],
                      skew_btmup[0], skew_btmup[1], style_set[4 + style_offset]]
        style_offset += 5
    leftist_recur_mean = [mean(leftist_recur[1])] * 2
    leftist_iter_mean = [mean(leftist_iter[1])] * 2
    skew_recur_mean = [mean(skew_recur[1])] * 2
    skew_iter_mean = [mean(skew_iter[1])] * 2
    skew_btmup_mean = [mean(skew_btmup[1])] * 2
    plot_data += [[0.000075], 'k--',
                  (0, 1000), leftist_recur_mean, 'r--',
                  (0, 1000), leftist_iter_mean, 'b--',
                  (0, 1000), skew_recur_mean, 'g--',
                  (0, 1000), skew_iter_mean, 'y--',
                  (0, 1000), skew_btmup_mean, 'm--']

    plt.plot(*plot_data)
    plt.legend(['leftist_recur', 'leftist_iter', 'skew_top_down_iter', 'skew_top_down_recur', 'skew_bottom_up', 'average'])
    plt.text(250, 0.00007, 'N = 100000')
    plt.xlabel('number of merge operations M')
    plt.ylabel(r'$\frac{\mathsf{time}}{\mathsf{M}}$ (s)')
    plt.title('time/M - M relationship on leftist and skew heaps')
    plt.savefig('time_merges.pdf', format='pdf', bbox_inches='tight', pad_inches=0.2)
    plt.savefig('time_merges', bbox_inches='tight', pad_inches=0.2)
    #plt.show()
    plt.clf()


def mean(seq):
    return float(sum(seq)) / len(seq)

def plot_time_size_leftist_skew(data, sorted_data=None, reversed_data=None,
                                semilog=False, ord_data=None):
    plot_data = []
    # legend data
    if sorted_data or reversed_data:
        plot_data += [[0], 'k-']
        if sorted_data:
            plot_data += [[0], 'k--']
        if reversed_data:
            plot_data += [[0], 'k:']

    leftist_iter = [(record.size, record.time)
                    for record in data
                    if record.method == 'leftist_iter']
    leftist_recur = [(record.size, record.time)
                     for record in data
                     if record.method == 'leftist_recur']
    skew_recur = [(record.size, record.time)
                  for record in data
                  if record.method == 'skew_recur']
    skew_iter = [(record.size, record.time)
                 for record in data
                 if record.method == 'skew_iter']
    skew_btmup = [(record.size, record.time)
                  for record in data
                  if record.method == 'skew_btmup']
    leftist_recur, leftist_iter, skew_recur, skew_iter, skew_btmup = zip(*leftist_recur), zip(*leftist_iter), zip(*skew_recur), zip(*skew_iter), zip(*skew_btmup)
    plot_data += [leftist_recur[0], leftist_recur[1], 'r-',
                 leftist_iter[0], leftist_iter[1], 'b-',
                 skew_recur[0], skew_recur[1], 'g-',
                 skew_iter[0], skew_iter[1], 'y-',
                 skew_btmup[0], skew_btmup[1], 'm-']

    if sorted_data:
        leftist_iter_sorted = [(record.size, record.time)
                               for record in sorted_data
                               if record.method == 'leftist_iter']
        leftist_recur_sorted = [(record.size, record.time)
                                for record in sorted_data
                                if record.method == 'leftist_recur']
        skew_recur_sorted = [(record.size, record.time)
                             for record in sorted_data
                             if record.method == 'skew_recur']
        skew_iter_sorted = [(record.size, record.time)
                            for record in sorted_data
                            if record.method == 'skew_iter']
        skew_btmup_sorted = [(record.size, record.time)
                             for record in sorted_data
                             if record.method == 'skew_btmup']
        leftist_recur_sorted, leftist_iter_sorted, skew_recur_sorted, skew_iter_sorted, skew_btmup_sorted = zip(*leftist_recur_sorted), zip(*leftist_iter_sorted), zip(*skew_recur_sorted), zip(*skew_iter_sorted), zip(*skew_btmup_sorted)
        plot_data += [leftist_recur_sorted[0], leftist_recur_sorted[1], 'r--',
                      leftist_iter_sorted[0], leftist_iter_sorted[1], 'b--',
                      skew_recur_sorted[0], skew_recur_sorted[1], 'g--',
                      skew_iter_sorted[0], skew_iter_sorted[1], 'y--',
                      skew_btmup_sorted[0], skew_btmup_sorted[1], 'm--']

    if reversed_data:
        leftist_iter_reversed = [(record.size, record.time)
                               for record in reversed_data
                               if record.method == 'leftist_iter']
        leftist_recur_reversed = [(record.size, record.time)
                                for record in reversed_data
                                if record.method == 'leftist_recur']
        skew_recur_reversed = [(record.size, record.time)
                             for record in reversed_data
                             if record.method == 'skew_recur']
        skew_iter_reversed = [(record.size, record.time)
                            for record in reversed_data
                            if record.method == 'skew_iter']
        skew_btmup_reversed = [(record.size, record.time)
                             for record in reversed_data
                             if record.method == 'skew_btmup']
        leftist_recur_reversed, leftist_iter_reversed, skew_recur_reversed, skew_iter_reversed, skew_btmup_reversed = zip(*leftist_recur_reversed), zip(*leftist_iter_reversed), zip(*skew_recur_reversed), zip(*skew_iter_reversed), zip(*skew_btmup_reversed)
        plot_data += [leftist_recur_reversed[0], leftist_recur_reversed[1], 'r:',
                      leftist_iter_reversed[0], leftist_iter_reversed[1], 'b:',
                      skew_recur_reversed[0], skew_recur_reversed[1], 'g:',
                      skew_iter_reversed[0], skew_iter_reversed[1], 'y:',
                      skew_btmup_reversed[0], skew_btmup_reversed[1], 'm:']

    if ord_data:
        ordinary = [(record.size, record.time)
                    for record in ord_data
                    if record.method == 'ordinary']
        ordinary = zip(*ordinary)
        plot_data += [ordinary[0], ordinary[1], 'c-']

    # begin plotting
    plt.plot(*plot_data)
    if semilog:
        plt.semilogx()
    if sorted_data and not reversed_data:
        #plt.semilogy()
        pass
    legend = []
    if sorted_data or reversed_data:
        legend += ['random']
        if sorted_data:
            legend += ['sorted']
        if reversed_data:
            legend += ['reversed']
    legend += ['leftist_recur', 'leftist_iter', 'skew_top_down_recur', 'skew_top_down_iter', 'skew_bottom_up']

    if ord_data: legend += ['ordinary']
    if sorted_data and not reversed_data:
        #plt.legend(legend, loc='lower right', fontsize='small')
        plt.legend(legend, loc='upper left')
    else:
        plt.legend(legend, loc='upper left')
    plt.xlabel('size')
    plt.ylabel('time (s)')
    plt.text(6000, 0.002, 'M = 100')
    if ord_data:
        plt.title('time - size relationship on differents heaps')
    else:
        plt.title('time - size relationship on leftist and skew heaps')

    if ord_data:
        fig_name = 'time_size_all'
    elif semilog:
        fig_name = 'time_size_leftist_skew_semilog'
    elif sorted_data and reversed_data:
        fig_name = 'time_size_leftist_skew_sorted_reversed'
    elif sorted_data and not reversed_data:
        fig_name = 'time_size_leftist_skew_sorted'
    elif not sorted_data and reversed_data:
        fig_name = 'time_size_leftist_skew_reversed'
    else:
        fig_name = 'time_size_leftist_skew'
    plt.savefig(fig_name + '.pdf', format='pdf')
    plt.savefig(fig_name)
    plt.clf()


def plot_leftist_iter(data):
    leftist = [(record.size, record.time)
               for record in data
               if record.method == 'leftist_iter']
    leftist = zip(*leftist)
    plot_data = [leftist[0], leftist[1], 'b-']

    plt.plot(*plot_data)
    plt.savefig('leftist_iter')
    plt.clf()


def leftist_skew_merge_amortized():
    data = read_data_leftist_skew(path='leftist_skew_merge_amortized.txt')
    plot_time_merges_leftist_skew(data)


def leftist_skew_time_size():
    data = read_data_leftist_skew(path='leftist_skew_time_size_random.txt')
    plot_time_size_leftist_skew(data)
    plot_time_size_leftist_skew(data, semilog=True)


def leftist_skew_time_size_sorted_reversed():
    data = read_data_leftist_skew(path='leftist_skew_time_size_random.txt')
    sorted_data = read_data_leftist_skew(path='leftist_skew_time_size_sorted.txt')
    reversed_data = read_data_leftist_skew(path='leftist_skew_time_size_reversed.txt')
    #plot_time_size_leftist_skew(data, sorted_data=sorted_data, reversed_data=reversed_data)
    plot_time_size_leftist_skew(data, sorted_data=sorted_data)
    #plot_time_size_leftist_skew(data, reversed_data=reversed_data)


def all_time_size():
    data = read_data_leftist_skew(path='leftist_skew_time_size_random.txt')
    ord_data = read_data_leftist_skew(path='time_size_ordinary.txt')
    plot_time_size_leftist_skew(data, ord_data=ord_data)


def time_ratio_ordinary():
    data = read_data_ordinary()
    plot_time_ratio_ordinary(data)


def main():
    #leftist_skew_merge_amortized()
    #leftist_skew_time_size()
    #leftist_skew_time_size_sorted_reversed()
    all_time_size()

if __name__ == '__main__':
    main()
