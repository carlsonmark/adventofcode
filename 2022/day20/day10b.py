test_input = """\
1
2
-3
3
-2
0
4
"""


def parse_input(s: str):
    return [int(l) * 811589153 for l in s.splitlines(keepends=False)]


def new_list(indexes, lst):
    return [lst[i] for i in indexes]


def mix_one(indexes, lst, index):
    lst_len = len(indexes)
    which = lst[index]
    old_index = indexes.index(index)
    offset = abs(which) % (lst_len - 1)
    if which < 0:
        offset = -offset
    new_index = old_index + offset
    if new_index >= lst_len:
        new_index = new_index % lst_len + 1
    elif new_index == 0:
        if which < 0:
            new_index = lst_len
    indexes.pop(old_index)
    indexes.insert(new_index, index)
    return indexes


def mix_all(lst, indexes):
    for i in range(len(lst)):
        indexes = mix_one(indexes, lst, index=i)
    print(lst)
    return indexes


def find_coordinates(lst):
    zero_pos = lst.index(0)
    lst_len = len(lst)
    pos_1000 = (zero_pos + 1000) % lst_len
    pos_2000 = (zero_pos + 2000) % lst_len
    pos_3000 = (zero_pos + 3000) % lst_len
    val_1000 = lst[pos_1000]
    val_2000 = lst[pos_2000]
    val_3000 = lst[pos_3000]
    print(f'{pos_1000=}, {pos_2000=}, {pos_3000=}')
    print(f'{val_1000=}, {val_2000=}, {val_3000=}')
    print(f'{val_1000 + val_2000 + val_3000 = }')
    return


lst_ = parse_input(test_input)
print(lst_)
indexes_ = list(range(len(lst_)))
for i in range(10):
    indexes_ = mix_all(lst_, indexes_)
find_coordinates(new_list(indexes_, lst_))

lst_ = parse_input(open('day20-input.txt').read())
indexes_ = list(range(len(lst_)))
for i in range(10):
    indexes_ = mix_all(lst_, indexes_)
find_coordinates(new_list(indexes_, lst_))

# indexes_ = list(range(len(lst_)))
# for i in range(len(lst_)):
#     indexes_ = mix_one(indexes_, lst_, index=i)
# find_coordinates(new_list(indexes_, lst_))
#
