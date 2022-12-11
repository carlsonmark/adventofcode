# Notes:
# Worry level is no longer divided by 3
# What is the score after 10000 rounds
# Numbers get stupidly large, so need to find a way to keep them low without breaking the algorithm
# First idea was to limit it to a mod of the product of all the test divisors. Seems to work.
# It was right, but I PEBKAC'd for a while because I was doing 10001 round :-(


import dataclasses
from typing import List, Union
import numpy as np

test_input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1

"""


@dataclasses.dataclass
class Monkey:
    number: int
    items: List[int]
    operation: str
    test_divisible_by: int
    test_true_monkey: int
    test_false_monkey: int
    # Inspection count
    score: int = 0
    operation_amount: Union[int, str] = ''
    # Limit item score to a modulus of:
    score_mod: int = 0

    def __post_init__(self):
        # Eval is too slow, create an apply_operation lambda
        self.operation_amount = self.operation.split(' ')[-1]
        if self.operation_amount != 'old':
            self.operation_amount = int(self.operation_amount)
        if '+' in self.operation:
            if self.operation_amount == 'old':
                self.apply_operation = self.apply_operation_plus_item
            else:
                self.apply_operation = self.apply_operation_plus_amount
        elif '*' in self.operation:
            if self.operation_amount == 'old':
                self.apply_operation = self.apply_operation_times_item
            else:
                self.apply_operation = self.apply_operation_times_amount
        else:
            raise Exception(self.operation)
        return

    def process_item(self, monkeys):
        self.score += 1
        item = self.items[0]
        self.items = self.items[1:]
        item = self.apply_operation(item)
        item %= self.score_mod
        test = (item % self.test_divisible_by) == 0
        if test:
            monkeys[self.test_true_monkey].items.append(item)
        else:
            monkeys[self.test_false_monkey].items.append(item)
        return

    def process_items(self, monkeys):
        while self.items:
            self.process_item(monkeys)
        return

    def apply_operation_times_item(self, item):
        return item * item

    def apply_operation_times_amount(self, item):
        return item * self.operation_amount

    def apply_operation_plus_item(self, item):
        return item + item

    def apply_operation_plus_amount(self, item):
        return item + self.operation_amount


def process_round(monkeys):
    for monkey in monkeys:
        monkey.process_items(monkeys)
    return


def print_inspections(monkeys):
    for monkey in monkeys:
        print(f'Monkey {monkey.number}: Inspected {monkey.score} items')
    return


def parse_monkeys(s):
    monkeys = []
    line_count = 0
    monkey_index = -1
    items = []
    operation = ''
    test = 0
    true_monkey = 0
    false_monkey = 0
    for line in s.splitlines(keepends=False):
        monkey_line = line_count % 7
        if monkey_line == 0:
            # Monkey index
            monkey_index += 1
        elif monkey_line == 1:
            # Item list
            item_list_str = line[len('  Starting items: '):]
            items = [int(item) for item in item_list_str.split(', ')]
        elif monkey_line == 2:
            # Operation
            operation = line[len('  Operation: new = '):]
        elif monkey_line == 3:
            # Test
            test = int(line[len('  Test: divisible by '):])
        elif monkey_line == 4:
            # if_true
            true_monkey = int(line[len('    If true: throw to monkey '):])
        elif monkey_line == 5:
            # if_true
            false_monkey = int(line[len('    If true: throw to monkey '):])
        else:
            monkeys.append(Monkey(
                number=monkey_index,
                items=items,
                operation=operation,
                test_divisible_by=test,
                test_true_monkey=true_monkey,
                test_false_monkey=false_monkey
            ))
        line_count += 1
    set_score_mod(monkeys)
    return monkeys


def set_score_mod(monkeys):
    mods = [monkey.test_divisible_by for monkey in monkeys]
    score_mod = np.product(mods)
    for monkey in monkeys:
        monkey.score_mod = score_mod
    return


def top_two_scores(monkeys):
    scores = list(sorted(monkey.score for monkey in monkeys))
    return scores[-2:]


monkeys = parse_monkeys(test_input)
for round in range(10000):
    process_round(monkeys)
    if (round % 1000 == 999) or round == 0 or round == 19:
        print(f'After round {round}')
        print_inspections(monkeys)
    # if round % 10 == 0:
    #     print(f'{round=}')
top_2 = top_two_scores(monkeys)
for i, monkey in enumerate(monkeys):
    print(f'Monkey {i} score={monkey.score}')
print(f'{top_2=}, {top_2[0] * top_2[1]=}')

monkeys = parse_monkeys(open('day11-input.txt').read())
for round in range(10000):
    process_round(monkeys)
top_2 = top_two_scores(monkeys)
for i, monkey in enumerate(monkeys):
    print(f'Monkey {i} score={monkey.score}')
print(f'{top_2=}, {top_2[0] * top_2[1]=}')
