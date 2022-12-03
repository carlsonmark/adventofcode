
lines = open('day1a-input.txt').readlines()
elves = []

elf_calories = 0
for line in lines:
    try:
        elf_calories += int(line.strip('\n'))
    except ValueError:
        elves.append(elf_calories)
        elf_calories = 0

sorted_elves = list(sorted(elves))
print(sorted_elves)
print(f'{sum(sorted_elves[-3:])=}')
