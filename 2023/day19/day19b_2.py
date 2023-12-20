import dataclasses
from copy import copy
from typing import List, Dict
from ranges import Range

# Sankey diagrams helped with debugging...
# Started trying to implement my own ranges using tuples... then I thought it
# might be better to use python-ranges... I would have been much better off
# implementing my own Range class. python-ranges can be inclusive or exclusive,
# but the results of the subtraction operation does not take that into account,
# so I had to have some really ugly workarounds.

# Don't even bother trying to read this code, it's horrible and I spent way too
# long on it to clean it up.


example = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}
"""

@dataclasses.dataclass
class Rule:
    # x, m, a, s
    variable: str
    # Comparison threshold
    threshold: int
    # Comparison: <, >
    comparison: str
    # A, R, or workflow name
    result: str
    @classmethod
    def from_str(cls, s: str):
        comparison = '>'
        if '<' in s:
            comparison = '<'
        variable, s = s.split(comparison)
        threshold_str, result = s.split(':')
        return Rule(variable, int(threshold_str), comparison, result)


@dataclasses.dataclass
class Workflow:
    name: str
    rules: List[Rule]
    # A, R, or workflow name
    result: str
    @classmethod
    def from_str(cls, line: str):
        name, rules_string = line[:-1].split('{')
        rules = []
        for rule_string in rules_string.split(','):
            if '>' in rule_string or '<' in rule_string:
                rules.append(Rule.from_str(rule_string))
            else:
                result = rule_string
        return Workflow(name, rules, result)

def parse(lines: str):
    workflows = []
    for line in lines.splitlines():
        if not line:
            break
        workflows.append(Workflow.from_str(line))
    return workflows


def sub_ranges(remaining, ranges_):
    one = copy(remaining)
    two = copy(remaining)
    for key, range_ in ranges_.items():
        new_range = one[key] - range_
        remainder = remaining[key] - new_range
        if new_range is None:
            start = remaining[key].start
            new_range = Range(start, start)
        else:
            if new_range < remainder:
                new_range.end -= 1
            else:
                new_range.start += 1
        one[key] = new_range
        # remainder = remaining[key] - new_range
        if remainder is None:
            end = remaining[key].end
            remainder = Range(end, end)
        else:
            # remainder.start += 1
            # remainder.end += 1
            pass
        two[key] = remainder

    return one, two


def to_subrange(comparison: str, result: str, key: str, value: int):
    # range_ = dict(x=(1, 4000), m=(1, 4000), a=(1, 4000), s=(1, 4000))
    range_ = {}
    if comparison == '<':
        if result == 'R':
            range_[key] = Range(value, 4000)
        else:
            range_[key] = Range(1, value-1)
    else:
        if result == 'R':
            range_[key] = Range(1, value)
        else:
            range_[key] = Range(value+1, 4000)
    return range_

def sum_remaining(remaining: Dict[str, Range]):
    count = 1
    for range_ in remaining.values():
        length = 1
        if range_ is not None:
            length += range_.length()
        count *= length
    return count

example000 = """\
in{s<1351:px,bbb}
bbb{m>999:A,R}
px{a<2006:ddd,m>2090:A,A}
ddd{a<2:A,A}
"""
example00 = """\
in{a>999:ccc,bbb}
bbb{m>999:ccc,R}
ccc{s>999:A,R}
"""
example0 = """\
in{x>999:A,a>999:ccc,bbb}
bbb{m>999:A,A}
ccc{s>999:A,A}
"""
example1 = """\
in{x>0:bbb,s>0:bbb,bbb}
bbb{m<4001:A,A}
"""
example2 = """\
in{x>3499:A,bbb}
bbb{m>999:A,R}
"""
example3 = """\
in{x>1999:A,R}
"""
example4 = """\
lnx{m>1548:A,A}
qs{s>3448:A,lnx}
in{s<1351:A,qqz}
qqz{s>2770:qs,m<1801:A,R}
"""


def pct(v): return 100*v/(4000**4)

def walk_all(workflow: Workflow, workflows: Dict[str, Workflow],
             remaining: Dict[str, Range],
             accepted: Dict[str, int],
             rejected: Dict[str, int],
             ):
    remaining_count = sum_remaining(remaining)
    # print(f'in {workflow.name}, {pct(remaining_count)=}')
    for rule in workflow.rules:
        if rule.result not in ('A', 'R'):
            sub = to_subrange(rule.comparison, rule.result, rule.variable,
                              rule.threshold)
            remaining, to_use = sub_ranges(remaining, sub)
            count = sum_remaining(to_use)
            remaining_count -= count
            print(f'{workflow.name} [{sum_remaining(to_use)}] {rule.result}')
            walk_all(workflows[rule.result], workflows, to_use, accepted, rejected)
        else:
            sub = to_subrange(rule.comparison, rule.result, rule.variable, rule.threshold)
            remaining, to_use = sub_ranges(remaining, sub)
            if rule.result == 'R':
                remaining, to_use = to_use, remaining
            count = sum_remaining(to_use)
            remaining_count -= count
            print(f'{workflow.name} [{sum_remaining(to_use)}] {rule.result}')
            if rule.result == 'A':
                # print(f'Accepted {workflow.name}, {pct(count)=}, {pct(remaining_count)=}, {pct(sum_remaining(remaining))=}')
                if workflow.name in accepted:
                    accepted[workflow.name] += count
                else:
                    accepted[workflow.name] = count
            else:
                # print(f'Rejected {workflow.name}, {pct(count)=}, {pct(remaining_count)=}')
                if workflow.name in rejected:
                    rejected[workflow.name] += count
                else:
                    rejected[workflow.name] = count
    remaining_count = sum_remaining(remaining)
    print(f'{workflow.name} [{sum_remaining(remaining)}] {workflow.result}')
    if workflow.result == 'A':
        # print(f'Accepted {workflow.name}, {pct(remaining_count)=}')
        if workflow.name in accepted:
            accepted[workflow.name] += remaining_count
        else:
            accepted[workflow.name] = remaining_count
    elif workflow.result == 'R':
        # print(f'Rejected {workflow.name}, {pct(remaining_count)=}')
        if workflow.name in rejected:
            rejected[workflow.name] += remaining_count
        else:
            rejected[workflow.name] = remaining_count
    else:
        walk_all(workflows[workflow.result], workflows, remaining, accepted,
                 rejected)
    return

def solve(lines: str):
    all_workflows = parse(lines)
    workflows = {
        workflow.name: workflow for workflow in all_workflows
    }
    full_range = dict(x=Range(1, 4000), m=Range(1, 4000), a=Range(1, 4000), s=Range(1, 4000))
    accepted = {}
    rejected = {}
    walk_all(workflows['in'], workflows, full_range, accepted, rejected)
    accepted_count = sum(accepted.values())
    rejected_count = sum(rejected.values())
    for k, v in accepted.items():
        print(f'A {k}: {pct(v)}')
    for k, v in rejected.items():
        print(f'R {k}: {pct(v)}')
    found = accepted_count + rejected_count
    expected = 4000 * 4000 * 4000 * 4000
    assert found == expected, f'{accepted_count} + {rejected_count} = {found} != {expected}, {100*found/expected:.3f}%'
    print(accepted_count)
    return

if __name__ == '__main__':
    # 167_409_079_868_000
    # 49_984_000_000_000
    # Tests
    assert 3000 == sum_remaining(to_subrange('<', 'R', 'x', 1001))
    assert 1000 == sum_remaining(to_subrange('<', 'A', 'x', 1001))
    assert 1000 == sum_remaining(to_subrange('>', 'R', 'x', 1000))
    assert 3000 == sum_remaining(to_subrange('>', 'A', 'x', 1000))
    assert 1 == sum_remaining(sub_ranges(dict(a=Range(1,4000)), dict(a=Range(2,4000)))[0])
    assert 3999 == sum_remaining(sub_ranges(dict(a=Range(1,4000)), dict(a=Range(2,4000)))[1])
    assert 1 == sum_remaining(sub_ranges(dict(a=Range(1,4000)), dict(a=Range(1,3999)))[0])
    assert 3999 == sum_remaining(sub_ranges(dict(a=Range(1,4000)), dict(a=Range(1,3999)))[1])
    assert (dict(a=Range(4000,4000)), dict(a=Range(1,3999))) == sub_ranges(dict(a=Range(1,4000)), dict(a=Range(1,3999)))
    assert (dict(a=Range(1,1)), dict(a=Range(2,4000))) == sub_ranges(dict(a=Range(1,4000)), dict(a=Range(2,4000)))
    solve(example)
    solve(open('input.txt').read())
