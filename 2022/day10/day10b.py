# Notes
# The x value is a sprite position on a screen
# Sprite is 3 pixels wide
# One pixel is drawn per cycle
# One line per 40 cycles
# Render the lines and find the 8 capital letters rendered

test_input = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""


def parse_instructions(lines):
    instructions = []
    for line in lines:
        if line == 'noop':
            instructions.append((line, ''))
        else:
            instructions.append(line.split(' '))
    return instructions


def execute_instruction(registers, instructions):
    global cycle_count
    # print(f'{cycle_count=}, X={registers["X"]}, {instructions[0]=}, {registers["delay"]=}')
    # If there is delay, count it down before executing
    if registers['delay']:
        registers['delay'] -= 1
        return instructions
    # No delay, execute this instruction and get delay for next instruction
    opcode, operand = instructions[0]
    if opcode == 'noop':
        pass
    else:
        registers['X'] += int(operand)
    instructions = instructions[1:]
    delay = 0
    if instructions and instructions[0][0] == 'addx':
        delay = 1
    registers['delay'] = delay
    return instructions


def render_pixel(registers):
    display_x = registers['display_x']
    x = registers['X']
    if abs(display_x - x) < 2:
        print('#', end='')
    else:
        print('.', end='')


def execute_cycle(registers, instructions):
    render_pixel(registers)
    instructions = execute_instruction(registers, instructions)
    return instructions


instructions = parse_instructions(test_input.splitlines(keepends=False))
registers = {
    'X': 1,
    'delay': 0 if instructions[0][0] == 'noop' else 1,
    'display_x': 0
}
cycle_count = 1
while instructions:
    instructions = execute_cycle(registers, instructions)
    cycle_count += 1
    registers['display_x'] += 1
    if registers['display_x'] >= 40:
        registers['display_x'] = 0
        print()

print()
print()
print()


instructions = parse_instructions(open('day10-input.txt').read().splitlines(keepends=False))
registers = {
    'X': 1,
    'delay': 0 if instructions[0][0] == 'noop' else 1,
    'display_x': 0
}
cycle_count = 1
while instructions:
    instructions = execute_cycle(registers, instructions)
    cycle_count += 1
    registers['display_x'] += 1
    if registers['display_x'] >= 40:
        registers['display_x'] = 0
        print()
