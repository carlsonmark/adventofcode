
lines = open('day1a-input.txt').readlines()
elves = []

elf_calories = 0
for line in lines:
    try:
        elf_calories += int(line.strip('\n'))
    except ValueError:
        elves.append(elf_calories)
        elf_calories = 0

print(elves)
print(f'{max(elves)=}')
