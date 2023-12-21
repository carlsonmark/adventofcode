import dataclasses
from copy import deepcopy
from typing import Dict, List

import numpy as np

# Ctrl+F'd the input.txt to see which things feed into rx, found 4 inputs.
# Check when these inputs each go low and find the LCM of all of them.
"""
&sl -> &ks -> hj
&rt -> &jf -> hj
&fv -> &qs -> hj
&gk -> &zk -> hj

&hj -> rx
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

def solve(lines: str):
    all_modules = parse(lines)
    # Spoiler: It's never going to go low in our lifetime with this code
    rx_low = False
    count = 0
    lcm_parts = {}
    while not rx_low:
        count += 1
        rx_low = push_button(all_modules, count, lcm_parts)
        if len(lcm_parts) == 4:
            values = list(lcm_parts.values())
            print(lcm_parts)
            lcm = np.lcm.reduce(values)
            print(f'{lcm=} for {lcm_parts}')
            break
    return

def push_button(all_modules, count: int, lcm_parts):
    pulse_queue.clear()
    pulse_queue.append(Pulse(False, 'button', 'broadcaster'))
    rx_low = False
    while pulse_queue:
        working_pulses = deepcopy(pulse_queue)
        pulse_queue.clear()
        for pulse in working_pulses:
            # print(pulse)
            if pulse.name_to in ('ks', 'jf', 'qs', 'zk'):
                if not pulse.high:
                    print(count, pulse)
                    if pulse.name_to not in lcm_parts:
                        lcm_parts[pulse.name_to] = count
            if pulse.name_from == 'rx':
                print('!!!!')
                print(pulse)
                print('!!!!')
                if not pulse.high:
                    rx_low = True
            module = all_modules.get(pulse.name_to, Output(pulse.name_to))
            module.recv_pulse(pulse.high, pulse.name_from)
    return rx_low

if __name__ == '__main__':
    solve(open('input.txt').read())
