
"""
256 boxes (lists)
- Means remove lens with the label if present, leaving the rest in order
=N Means replace the existing lens if it was there, otherwise add it to the end

Thankfully, Python dicts are ordered by default now
"""
from typing import Dict

example = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

def calc_hash(step: str) -> int:
    h = 0
    for c in step:
        h += ord(c)
        h *= 17
        h &= 0xff
    return h

def lens_label(lens: str):
    if lens[-1] == '-':
        # No number at the end
        return lens[:-1]
    # One digit at the end
    return lens[:-2]

def focal_length(lens: str) -> int:
    return int(lens[-1])

def remove_lens(box: Dict[str, str], lens: str):
    label = lens_label(lens)
    try:
        del box[label]
    except KeyError: pass
    return

def add_lens(box: Dict[str, str], lens: str):
    label = lens_label(lens)
    box[label] = lens
    return

def solve(s: str):
    lenses = s[:-1].split(',')
    boxes = [{} for _ in range(256)]

    for lens in lenses:
        box = calc_hash(lens_label(lens))
        remove = '-' in lens
        if remove:
            remove_lens(boxes[box], lens)
        else:
            add_lens(boxes[box], lens)

    focusing_power = 0
    for i, box in enumerate(boxes):
        box_score = i + 1
        for j, (label, lens) in enumerate(box.items()):
            slot_score = j + 1
            focusing_power += box_score * slot_score * focal_length(lens)
    print(f'{focusing_power=}')
    return

if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
