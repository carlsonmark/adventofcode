import dataclasses
from copy import deepcopy
from typing import Dict, List

example1 = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

example2 = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""

pulse_queue = []

@dataclasses.dataclass
class Pulse:
    high: bool
    name_from: str
    name_to: str
    def __str__(self):
        level = 'low'
        if self.high:
            level = 'high'
        return f'{self.name_from} -{level}-> {self.name_to}'

@dataclasses.dataclass
class FlipFlop:
    name: str = ''
    state: bool = False
    listeners: List[str] = dataclasses.field(default_factory=list)
    def recv_pulse(self, high: bool, module_name: str):
        # Only send the state when a low pulse is received
        if not high:
            self.state = not self.state
            for listener in self.listeners:
                pulse_queue.append(Pulse(self.state, self.name, listener))
        return
    def add_output(self, listener: str):
        self.listeners.append(listener)
        return


@dataclasses.dataclass
class Conjunction:
    name: str = ''
    inputs: Dict[str, bool] = dataclasses.field(default_factory=dict)
    listeners: List[str] = dataclasses.field(default_factory=list)
    def add_input(self, name: str):
        self.inputs[name] = False
        return
    def recv_pulse(self, high: bool, module_name: str):
        self.inputs[module_name] = high
        # Send low when all inputs are high, otherwise, send high
        to_send = not all(self.inputs.values())
        for listener in self.listeners:
            pulse_queue.append(Pulse(to_send, self.name, listener))
        return

@dataclasses.dataclass
class Broadcast:
    name: str = 'broadcaster'
    listeners: List[str] = dataclasses.field(default_factory=list)
    def recv_pulse(self, high: bool, module_name: str):
        for listener in self.listeners:
            pulse_queue.append(Pulse(high, self.name, listener))
        return

@dataclasses.dataclass
class Output:
    name: str = 'output'
    high_count: int = 0
    low_count: int = 0
    listeners: List[str] = dataclasses.field(default_factory=list) # Empty
    def recv_pulse(self, high: bool, module_name: str):
        if high:
            self.high_count += 1
        else:
            self.low_count += 1

def parse(lines: str):
    all_modules = {}
    # First, parse all the lines and add the modules
    for line in lines.splitlines():
        first, second = line.split(' -> ')
        if first.startswith('&'):
            module_type = Conjunction
            name = first[1:]
        elif line.startswith('%'):
            module_type = FlipFlop
            name = first[1:]
        else:
            module_type = Broadcast
            name = first
        listeners = second.split(', ')
        obj = module_type(name=name, listeners=listeners)
        all_modules[name] = obj
    # Now, for the conjunction modules, register the inputs
    for module in all_modules.values():
        if isinstance(module, Conjunction):
            for sender in all_modules.values():
                if module.name in sender.listeners:
                    module.add_input(sender.name)
    return all_modules

def solve(lines: str, repeat: int):
    all_modules = parse(lines)
    total_high = 0
    total_low = 0
    for _ in range(repeat):
        high_count, low_count = push_button(all_modules)
        total_high += high_count
        total_low += low_count
        print(f'This cycle: {high_count=}, {low_count=}, {total_high=}, {total_low=}')
        # for module in all_modules.values():
        #     print(module)
    print(total_high * total_low)
    return

def push_button(all_modules):
    high_count = 0
    low_count = 0
    pulse_queue.clear()
    pulse_queue.append(Pulse(False, 'button', 'broadcaster'))
    while pulse_queue:
        working_pulses = deepcopy(pulse_queue)
        pulse_queue.clear()
        for pulse in working_pulses:
            print(pulse)
            if pulse.high:
                high_count += 1
            else:
                low_count += 1
            module = all_modules.get(pulse.name_to, Output(pulse.name_to))
            module.recv_pulse(pulse.high, pulse.name_from)
    return high_count, low_count

if __name__ == '__main__':
    # solve(example1, repeat=1000)
    # solve(example2, repeat=1000)
    solve(open('input.txt').read(), repeat=1000)
