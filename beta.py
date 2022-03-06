import collections

t = [
    ['url1', 'hash1', 'path1', 'this1'], 
    ['url2', 'hash2', 'path2', 'this2'],
    ]
d = collections.OrderedDict()
d['a'] = 1
d['b'] = 2
d['c'] = 3
d['d'] = 4
d['e'] = 5
d['f'] = 6
d['g'] = 7
d['h'] = 8
d['i'] = 9
d['j'] = 10
print(d)
print(len(d))
print(len(t))
d_temp = d.copy()
while True:
    if 10 - len(d) >= len(t):
        print(d)
        for i in t:
            d[i[1]] = [i[2], i[3]]
        break
    else:
        pop_num = len(t) - (10 - len(d))
        print(pop_num)
        for i in d_temp.keys():
            if pop_num == 0:
                break
            else:
                d.pop(i)
                pop_num -= 1
print(d)
