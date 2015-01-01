import collections
import bisect

class Freq(object):
    def __init__(self, symbol, freq, is_leaf=True):
        self.symbol = symbol
        self.freq = freq
        self.is_leaf = is_leaf

    def left(self):
        if self.is_leaf:
            raise ValueError('A lefe node has no left tree')
        return self.symbol[0]

    def right(self):
        if self.is_leaf:
            raise ValueError('A lefe node has no right tree')
        return self.symbol[1]

    # Total ordering for binary search and insert for efficiency
    def __lt__(self, other):
        return self.freq < other.freq

    def __le__(self, other):
        return self.freq <= other.freq

    def __eq__(self, other):
        return self.freq == other.freq

    def __gt__(self, other):
        return self.freq > other.freq

    def __ge__(self, other):
        return self.freq >= other.freq

    def __ne__(self, other):
        return self.freq != other.freq

    def __repr__(self):
        res = '{}: {}'.format(self.symbol, self.freq)
        if self.is_leaf:
            res += 'L'
        return res


def merge(freq1, freq2):
    symbol = (freq1, freq2)
    freq = freq1.freq + freq2.freq
    return Freq(symbol, freq, False)


def get_freq_set(counter):
    freq_set = []
    for pair in counter:
        bisect.insort(freq_set, Freq(pair, counter[pair]))
    return freq_set


def huffman_tree(freq_set):
    tree = freq_set.copy()
    while len(tree) >= 2:
        min1 = tree.pop(0)
        min2 = tree.pop(0)
        node = merge(min1, min2)
        bisect.insort(tree, node)
    return tree.pop()


def gen_huffman_tree(string):
    counter = collections.Counter(string)
    freq_set = get_freq_set(counter)
    return huffman_tree(freq_set)


# Using a code table instead of a huffman tree for efficiency
def get_code_table(tree, encoded='', direction=''):
    if tree.is_leaf:
        if direction == '':    # in case there's only one character in the tree
            direction = '0'
        return {tree.symbol: encoded + direction}
    left_table = get_code_table(tree.left(), encoded=encoded + direction, direction='0')
    right_table = get_code_table(tree.right(), encoded=encoded + direction, direction='1')
    left_table.update(right_table)
    return left_table


def encode(string, tree=None, code_table=None):
    if tree is not None:
        code_table = get_code_table(tree)
    elif code_table is None:
        code_table = get_code_table(gen_huffman_tree(string))
    code = map(code_table.get, string)
    return "".join(code)


def decode(code, tree):
    if tree.is_leaf:    # only one character
        return tree.symbol * len(code)
    string = ''
    tmp_tree = tree
    for bit in code:
        if bit == '0':
            tmp_tree = tmp_tree.left()
        elif bit == '1':
            tmp_tree = tmp_tree.right()
        else:
            raise ValueError('Code can only contains 0 and 1, {} invalid'.format(bit))
        if tmp_tree.is_leaf:
            string += tmp_tree.symbol
            tmp_tree = tree
    return string


def main():
    test = """Enter the runtime context and return either this object or another object related to the runtime context. The value returned by this method is bound to the identifier in the as clause of with statements using this context manager."""
    tree = gen_huffman_tree(test)
    encoded = encode(test, tree)

    print(decode(encoded, tree))


if __name__ == '__main__':
    main()
