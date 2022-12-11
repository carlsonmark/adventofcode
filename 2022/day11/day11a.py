# Notes:
# Monkeys grabbed items and are tossing them amongst themselves
# They operate on a "worry level"
# "starting items" is a list of worry levels for each item they are holding in the order they will be inspected
# "operation" is how the worry level changes as they inspect each item
# "test" shows how the monkey will use the worry level to decide where to throw an item next
# After the monkey inspects the item, worry level is divide by 3 (truncated)
# A "turn" involves inspecting and throwing all of the items it is holding at a time, inthe order listed
# One monkey goes at a time, 0, 1, etc. This is a "round"
# When an item is thrown it goes on the end of the recipient monkey's list
# Keep track of number of times that a monkey inspects an item
# For the two monkeys with the highest inspection counts, solution is their inspection counts multiplied together

import dataclasses
from typing import List

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

    def process_item(self, monkeys):
        self.score += 1
        item = self.items[0]
        self.items = self.items[1:]
        item = self.apply_operation(item)
        item //= 3
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

    def apply_operation(self, item):
        new = eval(self.operation, dict(old=item))
        return new


def process_round(monkeys):
    for monkey in monkeys:
        monkey.process_items(monkeys)
    return


def print_items(monkeys):
    for monkey in monkeys:
        print(f'Monkey {monkey.number}: {monkey.items}')
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
    return monkeys


def top_two_scores(monkeys):
    scores = list(sorted(monkey.score for monkey in monkeys))
    return scores[-2:]


monkeys = parse_monkeys(test_input)
for round in range(20):
    process_round(monkeys)
    print(f'After round {round}')
    print_items(monkeys)
top_2 = top_two_scores(monkeys)
for i, monkey in enumerate(monkeys):
    print(f'Monkey {i} score={monkey.score}')
print(f'{top_2=}, {top_2[0] * top_2[1]=}')

monkeys = parse_monkeys(open('day11-input.txt').read())
for round in range(20):
    process_round(monkeys)
    print(f'After round {round}')
    print_items(monkeys)
top_2 = top_two_scores(monkeys)
for i, monkey in enumerate(monkeys):
    print(f'Monkey {i} score={monkey.score}')
print(f'{top_2=}, {top_2[0] * top_2[1]=}')
