import collections
from xlwt import *

Data = collections.namedtuple('Data', ['size', 'ratio', 'method', 'time'])    # define Data tuple

def read_data():
    SETTING, RESULT = 0, 1
    methods = {'0': 'insert', '1': 'buildheap'}

    data = []
    with open('result.txt', 'r') as f:
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
            tmp_time = line
            data.append(Data(tmp_size, tmp_ratio, tmp_method, tmp_time))
            line_state = SETTING
    return data


def separate_by_method(data):
    insert_data = filter(lambda record: record.method == 'insert', data)
    buildheap_data = filter(lambda record: record.method == 'buildheap', data)
    return insert_data, buildheap_data

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


def plot_data(data):
    import matplotlib.pyplot as plt
    size_set = (100, 1000, 10000, 100000, 1000000)
    method_set = ('insert', 'buildheap')
    style_set = ('r--', 'r:', 'b--', 'b:', 'g--', 'g:', 'c--', 'c:', 'm--', 'm:')
    plot_data = [[0], 'k--', [0], 'k:']    # initialize lines as black for a general legend

    # data -> curves
    style_index = 0
    for size in size_set:
        for method in method_set:
            ratio_time = [(record.ratio, record.time)
                          for record in data
                          if record.size == size and record.method == method]    # [(ratio1, time1), (ratio2, time2), ...]
            zipped_ratio_time = zip(*ratio_time)    # [(ratio1, ratio2, ...), (time1, time2, ...)]
            style = style_set[style_index]
            plot_data.extend([zipped_ratio_time[0], zipped_ratio_time[1], style])
            style_index += 1

    plt.plot(*plot_data)
    plt.semilogy()
    plt.xlabel(r'$\frac{\mathrm{\mathsf{heap1.size}}}{\mathrm{\mathsf{heap2.size}}}$', fontsize=20)
    plt.ylabel('time (s)')
    plt.title('time - ratio relationship of merging operation on ordinary heaps')
    plt.text(0.6, 0.02, r'$\mathrm{\mathsf{size=10^6}}$')
    plt.text(0.6, 0.002, r'$\mathrm{\mathsf{size=10^5}}$')
    plt.text(0.6, 0.0002, r'$\mathrm{\mathsf{size=10^4}}$')
    plt.text(0.6, 0.00002, r'$\mathrm{\mathsf{size=1,000}}$')
    plt.text(0.6, 0.000002, r'$\mathrm{\mathsf{size=100}}$')
    plt.legend(['insert', 'buildheap'], loc='upper left')
    plt.savefig('time_ratio_ordinary.pdf', format='pdf', bbox_inches='tight', pad_inches=0.2)
    plt.savefig('time_ratio_ordinary', bbox_inches='tight', pad_inches=0.2)
    #plt.show()

def main():
    data = read_data()
    #write_data(data)
    plot_data(data)

if __name__ == '__main__':
    main()
