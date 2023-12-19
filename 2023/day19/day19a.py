import dataclasses
from ast import literal_eval
from typing import List, Callable, Dict, Optional

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

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

@dataclasses.dataclass
class Part:
    x: int
    m: int
    a: int
    s: int
    @classmethod
    def from_str(cls, s: str):
        d_str = f'dict({s[1:-1]})'
        d = eval(d_str)
        return Part(**d)

    def rating(self) -> int:
        return self.x + self.m + self.a + self.s

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
    def decide(self, part: Part) -> Optional[str]:
        result = None
        value = vars(part)[self.variable]
        if self.comparison == '<':
            if value < self.threshold:
                return self.result
        else:
            if value > self.threshold:
                return self.result
        return result


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

    def decide(self, part: Part) -> str:
        for rule in self.rules:
            result = rule.decide(part)
            if result is not None:
                # Either 'A', 'R', or another workflow
                return result
        return self.result


def parse(lines: str):
    parsing_workflows = True
    workflows = []
    parts = []
    for line in lines.splitlines():
        if not line:
            parsing_workflows = False
            continue
        if parsing_workflows:
            workflows.append(Workflow.from_str(line))
        else:
            parts.append(Part.from_str(line))
    return workflows, parts

def accept_or_reject(workflows: Dict[str, Workflow], part: Part):
    workflow = workflows['in']
    decision = None
    while not decision:
        next_name = workflow.decide(part)
        if next_name in ('A', 'R'):
            decision = next_name
        else:
            workflow = workflows[next_name]
    return decision == 'A'

def solve(lines: str):
    all_workflows, parts = parse(lines)
    workflows = {
        workflow.name: workflow for workflow in all_workflows
    }
    accepted_list = []
    for part in parts:
        if accept_or_reject(workflows, part):
            accepted_list.append(part.rating())
    print(sum(accepted_list))
    return

if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
